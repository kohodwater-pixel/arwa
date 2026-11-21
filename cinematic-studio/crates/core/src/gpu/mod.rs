//! Cloud GPU manager: start/stop on demand, runtime and cost tracking, monthly budget, idle shutdown.
//!
//! Money rules enforced here (see GPU_COST_POLICY.md):
//!  - starting an instance needs an explicit approval flag and the approver's name, every time;
//!  - nothing in this module starts an instance on its own (no auto-start for queued jobs);
//!  - at 100% of the monthly budget, new generation jobs are refused and a start is refused;
//!  - stopping never needs approval, and an idle instance is stopped automatically.
pub mod runpod;

use crate::db::{self, new_id, now, row, rows};
use crate::error::{err, AppError, Result};
use crate::App;
use chrono::{DateTime, Datelike, TimeZone, Utc};
use rusqlite::{params, Connection};
use serde::Serialize;
use serde_json::{json, Value};

pub const DEFAULT_BUDGET_SAR: f64 = 1000.0;
pub const DEFAULT_USD_TO_SAR: f64 = 3.75;
pub const DEFAULT_IDLE_MINUTES: i64 = 10;

#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum GpuState {
    Running,
    Starting,
    Stopped,
    Error,
    Unknown,
}
#[derive(Debug, Clone, Serialize)]
pub struct InstanceStatus {
    pub state: GpuState,
    pub name: Option<String>,
    pub gpu: Option<String>,
    pub rate_usd_per_hour: Option<f64>,
    pub started_at: Option<String>,
}

pub trait GpuProvider: Send + Sync {
    fn id(&self) -> &'static str;
    fn status(&self, instance: &str) -> Result<InstanceStatus>;
    fn start(&self, instance: &str) -> Result<()>;
    fn stop(&self, instance: &str) -> Result<()>;
}

fn setting_f64(conn: &Connection, key: &str, default: f64) -> f64 {
    db::get_setting(conn, key).and_then(|v| v.parse::<f64>().ok()).filter(|v| v.is_finite() && *v >= 0.0).unwrap_or(default)
}
pub fn provider_id(conn: &Connection) -> String {
    db::get_setting(conn, "gpu_provider").unwrap_or_else(|| "none".into())
}
fn provider(app: &App) -> Result<(Box<dyn GpuProvider>, String)> {
    let (pid, instance, base) = { let c = app.db.lock().unwrap(); (provider_id(&c), db::get_setting(&c, "gpu_instance_id").unwrap_or_default(), db::get_setting(&c, "gpu_api_base")) };
    if pid != "runpod" { return err("gpu_not_configured", "no GPU provider is selected"); }
    if instance.trim().is_empty() { return err("gpu_not_configured", "no instance id is set"); }
    let key = app.secrets.get("gpu_api_key")?.filter(|k| !k.is_empty()).ok_or_else(|| AppError::new("gpu_not_configured", "no API key is stored"))?;
    Ok((Box::new(runpod::RunPod::new(key, base.as_deref())?), instance))
}

fn parse(ts: &str) -> Option<DateTime<Utc>> {
    DateTime::parse_from_rfc3339(ts).ok().map(|d| d.with_timezone(&Utc))
}
fn month_start(t: DateTime<Utc>) -> DateTime<Utc> {
    Utc.with_ymd_and_hms(t.year(), t.month(), 1, 0, 0, 0).single().unwrap_or(t)
}

/// Spend of the current calendar month (UTC), in SAR. A session still running counts up to this moment,
/// and a session that began last month counts only for the part inside this month.
pub fn month_spend(conn: &Connection, at: DateTime<Utc>) -> Result<(f64, f64)> {
    let from = month_start(at);
    let (mut sar, mut hours) = (0.0, 0.0);
    for s in rows(conn, "SELECT * FROM gpu_sessions WHERE stopped_at IS NULL OR stopped_at >= ?1", &[&from.to_rfc3339()])? {
        let Some(start) = s["started_at"].as_str().and_then(parse) else { continue };
        let end = s["stopped_at"].as_str().and_then(parse).unwrap_or(at);
        let h = (end - start.max(from)).num_milliseconds().max(0) as f64 / 3_600_000.0;
        hours += h;
        sar += h * s["rate_usd_per_hour"].as_f64().unwrap_or(0.0) * s["usd_to_sar"].as_f64().unwrap_or(DEFAULT_USD_TO_SAR);
    }
    Ok((sar, hours))
}

pub fn budget(conn: &Connection) -> Result<Value> {
    let limit = setting_f64(conn, "gpu_budget_sar", DEFAULT_BUDGET_SAR);
    let (spent, hours) = month_spend(conn, Utc::now())?;
    let percent = if limit > 0.0 { spent / limit * 100.0 } else { 100.0 };
    let level = if percent >= 100.0 { "blocked" } else if percent >= 90.0 { "warn90" } else if percent >= 70.0 { "warn70" } else { "ok" };
    Ok(json!({ "limit_sar": limit, "spent_sar": (spent * 100.0).round() / 100.0, "hours": (hours * 100.0).round() / 100.0, "percent": (percent * 10.0).round() / 10.0, "level": level,
        "remaining_sar": ((limit - spent).max(0.0) * 100.0).round() / 100.0, "usd_to_sar": setting_f64(conn, "usd_to_sar", DEFAULT_USD_TO_SAR), "month": Utc::now().format("%Y-%m").to_string() }))
}
/// New paid work is refused once the month's budget is used up. Only applies when a paid provider is selected.
pub fn assert_can_accept_jobs(conn: &Connection) -> Result<()> {
    if provider_id(conn) == "none" { return Ok(()); }
    if budget(conn)?["level"] == "blocked" {
        return err("budget_exceeded", "the monthly GPU budget is used up; new generation jobs are not accepted");
    }
    Ok(())
}

fn open_session(conn: &Connection) -> Result<Option<Value>> {
    row(conn, "SELECT * FROM gpu_sessions WHERE stopped_at IS NULL ORDER BY started_at DESC LIMIT 1", &[])
}
fn close_sessions(conn: &Connection, reason: &str) -> Result<()> {
    conn.execute("UPDATE gpu_sessions SET stopped_at = ?1, stop_reason = ?2 WHERE stopped_at IS NULL", params![now(), reason])?;
    Ok(())
}

/// Reads the provider's own status and reconciles the cost ledger with it, so time is charged for what
/// really ran, including an instance someone started or stopped outside the app.
pub fn sync(app: &App) -> Result<InstanceStatus> {
    let (p, instance) = provider(app)?;
    let st = p.status(&instance)?;
    let conn = app.db.lock().unwrap();
    let open = open_session(&conn)?;
    let billable = matches!(st.state, GpuState::Running | GpuState::Starting);
    if billable && open.is_none() {
        let rate = st.rate_usd_per_hour.unwrap_or_else(|| setting_f64(&conn, "gpu_rate_usd", 0.0));
        conn.execute("INSERT INTO gpu_sessions (id, provider, instance_id, started_at, rate_usd_per_hour, usd_to_sar, approved_by) VALUES (?1,?2,?3,?4,?5,?6,?7)",
            params![new_id(), p.id(), instance, st.started_at.clone().unwrap_or_else(now), rate, setting_f64(&conn, "usd_to_sar", DEFAULT_USD_TO_SAR), "not approved in the app (started elsewhere)"])?;
        db::audit(&conn, "warn", "gpu.external_start", "the instance is running but was not started from this app; its time is now being counted");
    } else if !billable && open.is_some() {
        close_sessions(&conn, "stopped outside the app")?;
        db::audit(&conn, "info", "gpu.external_stop", "the instance stopped outside the app");
    }
    Ok(st)
}

pub fn status(app: &App) -> Result<Value> {
    let (pid, instance, idle) = { let c = app.db.lock().unwrap(); (provider_id(&c), db::get_setting(&c, "gpu_instance_id").unwrap_or_default(), setting_f64(&c, "gpu_idle_minutes", DEFAULT_IDLE_MINUTES as f64)) };
    let configured = pid == "runpod" && !instance.is_empty() && app.secrets.get("gpu_api_key")?.is_some();
    let (live, error) = if configured { match sync(app) { Ok(s) => (Some(s), None), Err(e) => (None, Some(json!({ "code": e.code, "message": e.message }))) } } else { (None, None) };
    let conn = app.db.lock().unwrap();
    let session = open_session(&conn)?;
    let runtime_minutes = session.as_ref().and_then(|s| s["started_at"].as_str().and_then(parse)).map(|t| (Utc::now() - t).num_seconds() as f64 / 60.0);
    Ok(json!({ "provider": pid, "instance_id": instance, "configured": configured, "key_stored": app.secrets.get("gpu_api_key")?.is_some(), "secret_backend": app.secrets.backend(),
        "instance": live, "error": error, "session": session, "runtime_minutes": runtime_minutes, "idle_minutes": idle, "budget": budget(&conn)?,
        "sessions": rows(&conn, "SELECT * FROM gpu_sessions ORDER BY started_at DESC LIMIT 50", &[])? }))
}

/// Starts the instance. `approved` must be true and `approved_by` must name the person: the UI asks every time.
pub fn start(app: &App, approved: bool, approved_by: &str) -> Result<Value> {
    if !approved || approved_by.trim().len() < 2 {
        return err("approval_required", "starting a paid GPU needs an explicit approval and the approver's name");
    }
    {
        let conn = app.db.lock().unwrap();
        if budget(&conn)?["level"] == "blocked" { return err("budget_exceeded", "the monthly GPU budget is used up; raise the limit in the cost settings to continue"); }
    }
    let (p, instance) = provider(app)?;
    let before = p.status(&instance)?;
    if before.state != GpuState::Running && before.state != GpuState::Starting {
        p.start(&instance)?;
    }
    let conn = app.db.lock().unwrap();
    if open_session(&conn)?.is_none() {
        let rate = before.rate_usd_per_hour.unwrap_or_else(|| setting_f64(&conn, "gpu_rate_usd", 0.0));
        conn.execute("INSERT INTO gpu_sessions (id, provider, instance_id, started_at, rate_usd_per_hour, usd_to_sar, approved_by) VALUES (?1,?2,?3,?4,?5,?6,?7)",
            params![new_id(), p.id(), instance, now(), rate, setting_f64(&conn, "usd_to_sar", DEFAULT_USD_TO_SAR), crate::args::limit(approved_by.trim(), 80)])?;
    }
    db::set_setting(&conn, "gpu_last_activity", &now())?;
    db::audit(&conn, "info", "gpu.start", &format!("start approved by {}", crate::args::limit(approved_by.trim(), 80)));
    Ok(json!({ "ok": true }))
}

pub fn stop(app: &App, reason: &str) -> Result<Value> {
    let (p, instance) = provider(app)?;
    p.stop(&instance)?;
    let conn = app.db.lock().unwrap();
    close_sessions(&conn, reason)?;
    db::audit(&conn, "info", "gpu.stop", reason);
    Ok(json!({ "ok": true }))
}

pub fn touch_activity(conn: &Connection) {
    let _ = db::set_setting(conn, "gpu_last_activity", &now());
}

/// Called by the background worker: stops the instance when nothing has used it for the configured time.
pub fn idle_check(app: &App) -> Result<bool> {
    let due = {
        let conn = app.db.lock().unwrap();
        if provider_id(&conn) != "runpod" || open_session(&conn)?.is_none() { return Ok(false); }
        let active: i64 = conn.query_row("SELECT COUNT(*) FROM jobs WHERE kind = 'generate' AND status IN ('queued','submitted','running','downloading')", [], |r| r.get(0))?;
        let idle = setting_f64(&conn, "gpu_idle_minutes", DEFAULT_IDLE_MINUTES as f64);
        let last = db::get_setting(&conn, "gpu_last_activity").and_then(|t| parse(&t)).or_else(|| open_session(&conn).ok().flatten().and_then(|s| s["started_at"].as_str().and_then(parse)));
        active == 0 && idle > 0.0 && last.map(|t| (Utc::now() - t).num_seconds() as f64 >= idle * 60.0).unwrap_or(false)
    };
    if due {
        stop(app, "automatic idle shutdown")?;
    }
    Ok(due)
}
