//! Typed access to the JSON arguments of a command.
use crate::error::{AppError, Result};
use serde_json::Value;

pub fn str_req<'a>(v: &'a Value, key: &str) -> Result<&'a str> {
    v.get(key).and_then(Value::as_str).filter(|s| !s.trim().is_empty()).ok_or_else(|| AppError::new("bad_request", format!("missing text field: {key}")))
}
pub fn str_opt<'a>(v: &'a Value, key: &str) -> Option<&'a str> {
    v.get(key).and_then(Value::as_str)
}
pub fn i64_opt(v: &Value, key: &str) -> Option<i64> {
    v.get(key).and_then(|x| x.as_i64().or_else(|| x.as_f64().map(|f| f.round() as i64)))
}
pub fn f64_opt(v: &Value, key: &str) -> Option<f64> {
    v.get(key).and_then(Value::as_f64)
}
pub fn bool_opt(v: &Value, key: &str) -> Option<bool> {
    v.get(key).and_then(Value::as_bool)
}
pub fn limit(text: &str, max: usize) -> String {
    text.chars().take(max).collect()
}
pub fn one_of(value: &str, allowed: &[&str], field: &str) -> Result<()> {
    if allowed.contains(&value) { Ok(()) } else { Err(AppError::new("bad_request", format!("{field} must be one of: {}", allowed.join(", ")))) }
}
