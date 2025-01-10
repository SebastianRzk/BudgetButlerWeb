use crate::budgetbutler::view::request_handler::Redirect;
use crate::io::online::routes::offline_login_route;
use crate::model::local::LocalServerName;
use crate::model::remote::server::ServerConfiguration;

pub fn request_login(
    server_configuration: &ServerConfiguration,
    local_server_name: &LocalServerName,
) -> Redirect {
    Redirect::to(offline_login_route(server_configuration, local_server_name).as_str())
}

#[cfg(test)]
mod tests {
    use crate::io::online::login::request_login;
    use crate::model::local::LocalServerName;
    use crate::model::remote::server::ServerConfiguration;

    #[test]
    fn test_should_generate_offline_login_url() {
        let server_config = ServerConfiguration {
            server_url: "MyServerUrl".to_string(),
        };

        let result = request_login(
            &server_config,
            &LocalServerName {
                protocol: "http".to_string(),
                app_domain: "localhost".to_string(),
                app_port: 8080,
            },
        );

        assert_eq!(
            result.target,
            "MyServerUrl/offlinelogin?redirect=http://localhost:8080"
        )
    }
}
