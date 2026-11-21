//! Secrets (GPU provider API key, ComfyUI access token) never reach the web view, the database or the logs.
//! On Windows they live in the Windows Credential Manager (encrypted by the OS for the signed-in user).
use crate::error::{AppError, Result};
use std::collections::HashMap;
use std::sync::Mutex;

pub trait SecretStore: Send + Sync {
    fn set(&self, name: &str, value: &str) -> Result<()>;
    fn get(&self, name: &str) -> Result<Option<String>>;
    fn delete(&self, name: &str) -> Result<()>;
    fn backend(&self) -> &'static str;
}

pub const ALLOWED: [&str; 2] = ["comfy_token", "gpu_api_key"];
pub fn check_name(name: &str) -> Result<()> {
    if ALLOWED.contains(&name) { Ok(()) } else { Err(AppError::new("bad_secret_name", "unknown secret")) }
}

/// Process-memory store: used by tests and by the development bridge. Nothing is written to disk.
#[derive(Default)]
pub struct MemoryStore(Mutex<HashMap<String, String>>);
impl SecretStore for MemoryStore {
    fn set(&self, name: &str, value: &str) -> Result<()> {
        self.0.lock().unwrap().insert(name.into(), value.into());
        Ok(())
    }
    fn get(&self, name: &str) -> Result<Option<String>> {
        Ok(self.0.lock().unwrap().get(name).cloned())
    }
    fn delete(&self, name: &str) -> Result<()> {
        self.0.lock().unwrap().remove(name);
        Ok(())
    }
    fn backend(&self) -> &'static str {
        "memory (not persisted)"
    }
}

#[cfg(windows)]
pub struct CredentialManager;
#[cfg(windows)]
impl CredentialManager {
    fn entry(name: &str) -> Result<keyring::Entry> {
        keyring::Entry::new("Cinematic Studio", name).map_err(|e| AppError::new("secret_store", e.to_string()))
    }
}
#[cfg(windows)]
impl SecretStore for CredentialManager {
    fn set(&self, name: &str, value: &str) -> Result<()> {
        Self::entry(name)?.set_password(value).map_err(|e| AppError::new("secret_store", e.to_string()))
    }
    fn get(&self, name: &str) -> Result<Option<String>> {
        match Self::entry(name)?.get_password() {
            Ok(v) => Ok(Some(v)),
            Err(keyring::Error::NoEntry) => Ok(None),
            Err(e) => Err(AppError::new("secret_store", e.to_string())),
        }
    }
    fn delete(&self, name: &str) -> Result<()> {
        match Self::entry(name)?.delete_credential() {
            Ok(()) | Err(keyring::Error::NoEntry) => Ok(()),
            Err(e) => Err(AppError::new("secret_store", e.to_string())),
        }
    }
    fn backend(&self) -> &'static str {
        "Windows Credential Manager"
    }
}

pub fn default_store() -> Box<dyn SecretStore> {
    #[cfg(windows)]
    {
        Box::new(CredentialManager)
    }
    #[cfg(not(windows))]
    {
        Box::new(MemoryStore::default())
    }
}

/// Removes anything that looks like a credential from text before it is logged or shown.
pub fn redact(text: &str, secrets: &[Option<String>]) -> String {
    let mut out = text.to_string();
    for s in secrets.iter().flatten() {
        if s.len() >= 6 {
            out = out.replace(s.as_str(), "[redacted]");
        }
    }
    out
}
