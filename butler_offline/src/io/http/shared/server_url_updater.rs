use crate::io::disk::configuration::updater::update_configuration;
use crate::model::remote::server::ServerConfiguration;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::RootPath;
use actix_web::web::Data;

pub fn update_server_url(
    new_server_url: String,
    config: Data<ConfigurationData>,
    root_path: &Data<RootPath>,
) -> ServerConfiguration {
    let verarbeitet = verarbeite_server_url(new_server_url);

    let mut config = config.configuration.lock().unwrap();
    config.server_configuration = ServerConfiguration {
        server_url: verarbeitet,
    };
    let clone = config.server_configuration.clone();
    let refreshed_config = update_configuration(&root_path.path, config.clone());
    *config = refreshed_config;
    drop(config);
    clone
}

fn verarbeite_server_url(server_url: String) -> String {
    let mut verarbeitet = server_url;
    if !verarbeitet.starts_with("http://") && !verarbeitet.starts_with("https://") {
        verarbeitet = format!("https://{}", verarbeitet);
    }

    if verarbeitet.ends_with("/") {
        verarbeitet = verarbeitet[..verarbeitet.len() - 1].to_string();
    }

    verarbeitet
}

#[cfg(test)]
mod tests {
    use super::verarbeite_server_url;

    #[test]
    fn should_append_https_to_server_url() {
        let server_url = "myserver";
        let result = verarbeite_server_url(server_url.to_string());
        assert_eq!(result, "https://myserver");
    }

    #[test]
    fn should_remove_trailing_slash_to_server_url() {
        let server_url = "https://myserver/";
        let result = verarbeite_server_url(server_url.to_string());
        assert_eq!(result, "https://myserver");
    }

    #[test]
    fn should_allow_http() {
        let server_url = "http://myserver";
        let result = verarbeite_server_url(server_url.to_string());
        assert_eq!(result, server_url);
    }
}
