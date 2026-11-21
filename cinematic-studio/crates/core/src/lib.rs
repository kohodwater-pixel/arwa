//! Cinematic Studio core. Everything the desktop app does lives here, behind one entry point
//! (`rpc::dispatch`), with no dependency on Tauri or on a window. The Tauri shell is a thin wrapper.
pub mod args;
pub mod comfy;
pub mod db;
pub mod error;
pub mod files;
pub mod ffmpeg;
pub mod gpu;
pub mod jobs;
pub mod lora;
pub mod media;
pub mod paths;
pub mod projects;
pub mod rpc;
pub mod secrets;
pub mod timeline;

use error::{AppError, Result};
use paths::Library;
use rusqlite::Connection;
use secrets::SecretStore;
use std::path::{Path, PathBuf};
use std::sync::atomic::AtomicBool;
use std::sync::{Arc, Mutex, RwLock};

pub struct App {
    pub db: Mutex<Connection>,
    pub library: RwLock<Library>,
    pub secrets: Box<dyn SecretStore>,
    pub config_file: PathBuf,
    pub bundled_tools: Option<PathBuf>,
    /// True when the previous session did not shut down cleanly.
    pub recovered: bool,
    pub recovered_jobs: usize,
    pub shutting_down: AtomicBool,
}

#[derive(serde::Serialize, serde::Deserialize, Default)]
struct BootConfig {
    library_root: Option<String>,
}

impl App {
    /// `config_dir` holds only the pointer to the library (so the library can live anywhere and survives uninstall).
    pub fn start(config_dir: &Path, secrets: Box<dyn SecretStore>, bundled_tools: Option<PathBuf>) -> Result<Arc<App>> {
        std::fs::create_dir_all(config_dir)?;
        let config_file = config_dir.join("config.json");
        let boot: BootConfig = std::fs::read_to_string(&config_file).ok().and_then(|s| serde_json::from_str(&s).ok()).unwrap_or_default();
        let root = boot.library_root.map(PathBuf::from).unwrap_or_else(paths::default_library_root);
        let library = Library::open(&root)?;
        let conn = db::open(&library.db_file())?;
        let (recovered, recovered_jobs) = Self::recover(&conn)?;
        db::set_setting(&conn, "session_open", "1")?;
        Ok(Arc::new(App { db: Mutex::new(conn), library: RwLock::new(library), secrets, config_file, bundled_tools, recovered, recovered_jobs, shutting_down: AtomicBool::new(false) }))
    }

    /// Crash recovery. SQLite (WAL) already holds every edit, so no project data is lost; what needs repair is
    /// work that was in flight: those jobs go back to the queue and re-attach to the server by their remote id.
    fn recover(conn: &Connection) -> Result<(bool, usize)> {
        let unclean = db::get_setting(conn, "session_open").as_deref() == Some("1");
        let n = conn.execute("UPDATE jobs SET status = 'queued', stage = 'resumed after restart' WHERE status IN ('submitted', 'running', 'downloading')", [])?;
        conn.execute("UPDATE jobs SET status = 'failed', error = 'interrupted: the app closed during export', finished_at = ?1 WHERE kind = 'export' AND status = 'queued' AND stage = 'resumed after restart'", [db::now()])?;
        if unclean {
            db::audit(conn, "warn", "recovery", &format!("previous session ended unexpectedly; {n} job(s) resumed"));
        }
        Ok((unclean, n))
    }

    pub fn shutdown(&self) {
        self.shutting_down.store(true, std::sync::atomic::Ordering::SeqCst);
        if let Ok(conn) = self.db.lock() {
            let _ = db::set_setting(&conn, "session_open", "0");
            let _ = conn.execute_batch("PRAGMA wal_checkpoint(TRUNCATE);");
        }
    }

    pub fn lib(&self) -> Library {
        self.library.read().unwrap().clone()
    }

    pub fn tools(&self) -> Result<ffmpeg::Tools> {
        let configured = { db::get_setting(&self.db.lock().unwrap(), "ffmpeg_dir") };
        ffmpeg::locate(configured.as_deref(), self.bundled_tools.as_deref()).ok_or_else(|| AppError::new("ffmpeg_missing", "FFmpeg was not found. Set its folder in Settings."))
    }

    /// Points the app at another library folder (created if needed). Existing libraries are left where they are.
    pub fn set_library(&self, root: &Path) -> Result<()> {
        let library = Library::open(root)?;
        let conn = db::open(&library.db_file())?;
        db::set_setting(&conn, "session_open", "1")?;
        {
            let old = self.db.lock().unwrap();
            let _ = db::set_setting(&old, "session_open", "0");
        }
        std::fs::write(&self.config_file, serde_json::to_string_pretty(&BootConfig { library_root: Some(library.root.to_string_lossy().to_string()) })?)?;
        *self.db.lock().unwrap() = conn;
        *self.library.write().unwrap() = library;
        Ok(())
    }
}
