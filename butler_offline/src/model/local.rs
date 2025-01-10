pub struct LocalServerName {
    pub app_domain: String,
    pub app_port: u16,
    pub protocol: String,
}

pub const PRIVATE_DOMAIN: &str = "localhost";
pub const PUBLIC_DOMAIN: &str = "0.0.0.0";

pub const DEFAULT_APP_NAME: &str = "localhost";
pub const DEFAULT_APP_PORT: u16 = 5000;
pub const DEFAULT_PROTOCOL: &str = "http";

pub fn get_port_binding_domain(app_name: String) -> &'static str {
    if app_name == DEFAULT_APP_NAME {
        eprintln!("Running in private mode");
        return PRIVATE_DOMAIN;
    }
    eprintln!("Running in public mode");
    PUBLIC_DOMAIN
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_port_binding_domain() {
        let app_name = String::from(DEFAULT_APP_NAME);
        let result = get_port_binding_domain(app_name);
        assert_eq!(result, PRIVATE_DOMAIN);

        let app_name = String::from("test");
        let result = get_port_binding_domain(app_name);
        assert_eq!(result, PUBLIC_DOMAIN);
    }
}
