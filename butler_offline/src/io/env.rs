use std::env::VarError;

pub const ENV_APP_ROOT: &str = "BUDGETBUTLER_APP_ROOT";
pub const ENV_APP_PROTOCOL: &str = "BUDGETBUTLER_APP_PROTOCOL";
pub const ENV_APP_PORT: &str = "BUDGETBUTLER_APP_PORT";

pub fn get_env(key: &str) -> Result<String, VarError> {
    std::env::var(key)
}
