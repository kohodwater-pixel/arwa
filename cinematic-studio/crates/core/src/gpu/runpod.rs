//! RunPod provider, REST API v2.
//! Source: runpod/docs @ e4b64f1, api-reference-v2/openapi.json, read 2026-11-21 (v1 was retired on 2026-11-15):
//!   GET  /v2/pods/{id}          → status PROVISIONING | STARTING | RUNNING | EXITED | ERROR, cost (USD per hour), startedAt
//!   POST /v2/pods/{id}/action   {"action": "start" | "stop"}
//!   Authorization: Bearer <API key>
//! Not exercised against the live API (no key was available when this was written).
use super::{GpuProvider, GpuState, InstanceStatus};
use crate::error::{err, AppError, Result};
use serde_json::{json, Value};
use std::time::Duration;

pub struct RunPod {
    key: String,
    base: String,
    agent: ureq::Agent,
}
impl RunPod {
    pub fn new(key: String, base_override: Option<&str>) -> Result<Self> {
        let base = base_override.filter(|b| !b.trim().is_empty()).unwrap_or("https://api.runpod.io").trim_end_matches('/').to_string();
        // the override exists for tests; outside localhost it must still be https
        crate::comfy::client::validate_url(&base)?;
        Ok(Self { key, base, agent: ureq::AgentBuilder::new().timeout(Duration::from_secs(30)).redirects(0).build() })
    }
    fn check_id(id: &str) -> Result<()> {
        if id.is_empty() || id.len() > 64 || !id.chars().all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '_') { return err("bad_instance_id", "the pod id has unexpected characters"); }
        Ok(())
    }
    fn map(e: ureq::Error) -> AppError {
        match e {
            ureq::Error::Status(401, _) | ureq::Error::Status(403, _) => AppError::new("gpu_auth", "the GPU provider refused the API key"),
            ureq::Error::Status(404, _) => AppError::new("gpu_not_found", "the provider does not know this instance id"),
            ureq::Error::Status(429, _) => AppError::new("gpu_rate_limited", "the provider is rate limiting requests"),
            ureq::Error::Status(c, r) => AppError::new("gpu_error", format!("HTTP {c}: {}", r.into_string().unwrap_or_default().chars().take(300).collect::<String>())),
            ureq::Error::Transport(t) => AppError::new("gpu_unreachable", t.to_string()),
        }
    }
    fn action(&self, id: &str, action: &str) -> Result<()> {
        Self::check_id(id)?;
        self.agent.post(&format!("{}/v2/pods/{id}/action", self.base)).set("Authorization", &format!("Bearer {}", self.key)).send_json(json!({ "action": action })).map_err(Self::map)?;
        Ok(())
    }
}
impl GpuProvider for RunPod {
    fn id(&self) -> &'static str { "runpod" }
    fn status(&self, id: &str) -> Result<InstanceStatus> {
        Self::check_id(id)?;
        let j: Value = self.agent.get(&format!("{}/v2/pods/{id}", self.base)).set("Authorization", &format!("Bearer {}", self.key)).call().map_err(Self::map)?.into_json().map_err(|e| AppError::new("gpu_error", e.to_string()))?;
        let state = match j["status"].as_str().unwrap_or("") {
            "RUNNING" => GpuState::Running,
            "PROVISIONING" | "STARTING" => GpuState::Starting,
            "EXITED" | "TERMINATED" | "STOPPED" => GpuState::Stopped,
            "ERROR" => GpuState::Error,
            _ => GpuState::Unknown,
        };
        let gpu = j["gpu"]["displayName"].as_str().or_else(|| j["gpu"]["id"].as_str()).or_else(|| j["gpu"]["type"].as_str()).map(String::from);
        Ok(InstanceStatus { state, name: j["name"].as_str().map(String::from), gpu, rate_usd_per_hour: j["cost"].as_f64(), started_at: j["startedAt"].as_str().map(String::from) })
    }
    fn start(&self, id: &str) -> Result<()> { self.action(id, "start") }
    fn stop(&self, id: &str) -> Result<()> { self.action(id, "stop") }
}
