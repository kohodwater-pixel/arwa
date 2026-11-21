//! Library layout on disk and the only functions allowed to turn untrusted names into paths.
use crate::error::{err, Result};
use std::path::{Component, Path, PathBuf};

pub const SUBDIRS: [&str; 6] = ["Projects", "Assets", "Models", "Cache", "Logs", "Backups"];

#[derive(Debug, Clone)]
pub struct Library {
    pub root: PathBuf,
}
impl Library {
    /// Creates the folder structure if it is missing. Existing content is never touched.
    pub fn open(root: &Path) -> Result<Self> {
        if !root.is_absolute() {
            return err("bad_path", "the library location must be an absolute path");
        }
        std::fs::create_dir_all(root)?;
        for d in SUBDIRS {
            std::fs::create_dir_all(root.join(d))?;
        }
        Ok(Self { root: root.canonicalize()? })
    }
    pub fn dir(&self, name: &str) -> PathBuf {
        self.root.join(name)
    }
    pub fn db_file(&self) -> PathBuf {
        self.root.join("cinematic-studio.db")
    }
    /// Joins a relative path stored in the database onto the library root, refusing anything that escapes it.
    pub fn resolve(&self, relative: &str) -> Result<PathBuf> {
        safe_join(&self.root, relative)
    }
    pub fn relative(&self, absolute: &Path) -> Result<String> {
        let p = absolute.strip_prefix(&self.root).map_err(|_| crate::error::AppError::new("bad_path", "path is outside the library"))?;
        Ok(p.to_string_lossy().replace('\\', "/"))
    }
    pub fn contains(&self, p: &Path) -> bool {
        p.canonicalize().map(|c| c.starts_with(&self.root)).unwrap_or(false)
    }
}

/// Path traversal guard: only plain components are accepted (no `..`, no root, no drive prefix).
pub fn safe_join(root: &Path, relative: &str) -> Result<PathBuf> {
    let rel = Path::new(relative);
    if relative.is_empty() || relative.contains('\0') {
        return err("bad_path", "empty or invalid path");
    }
    let mut out = root.to_path_buf();
    for c in rel.components() {
        match c {
            Component::Normal(part) => out.push(part),
            Component::CurDir => {}
            _ => return err("bad_path", "path leaves its folder"),
        }
    }
    Ok(out)
}

/// A file or folder name made only of safe characters (used for project folders and generated files).
pub fn slug(name: &str, max: usize) -> String {
    let mut s = String::new();
    for ch in name.trim().chars() {
        if ch.is_alphanumeric() {
            s.push(ch);
        } else if (ch == ' ' || ch == '-' || ch == '_') && !s.ends_with('-') {
            s.push('-');
        }
        if s.chars().count() >= max {
            break;
        }
    }
    let s = s.trim_matches('-').to_string();
    // Windows reserved device names
    const RESERVED: [&str; 8] = ["con", "prn", "aux", "nul", "com1", "com2", "lpt1", "lpt2"];
    if s.is_empty() || RESERVED.contains(&s.to_lowercase().as_str()) {
        "project".to_string()
    } else {
        s
    }
}

pub fn default_library_root() -> PathBuf {
    let home = std::env::var_os("USERPROFILE").or_else(|| std::env::var_os("HOME")).map(PathBuf::from).unwrap_or_else(|| PathBuf::from("."));
    home.join("Documents").join("Cinematic Studio")
}
