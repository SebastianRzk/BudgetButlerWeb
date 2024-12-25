use crate::budgetbutler::view::request_handler::Redirect;
use crate::io::online::routes::offline_login_route;
use crate::model::remote::server::ServerConfiguration;

pub fn request_login(server_configuration: &ServerConfiguration) -> Redirect {
    Redirect::to(offline_login_route(server_configuration).as_str())
}

#[cfg(test)]
mod tests {
    use crate::io::online::login::request_login;
    use crate::model::remote::server::ServerConfiguration;

    #[test]
    fn test_should_generate_offline_login_url() {
        let server_config = ServerConfiguration {
            server_url: "MyServerUrl".to_string(),
        };

        let result = request_login(&server_config);

        assert_eq!(result.target, "MyServerUrl/offlinelogin")
    }
}
