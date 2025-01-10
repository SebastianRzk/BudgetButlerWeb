use crate::io::online::request::{get_request, ErrorOnRequest};
use crate::io::online::routes::einzelbuchungen_route;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::remote::login::LoginCredentials;
use crate::model::remote::server::ServerConfiguration;
use serde::Deserialize;

pub async fn request_einzelbuchungen(
    server_configuration: &ServerConfiguration,
    login_credentials: LoginCredentials,
) -> Result<Vec<Einzelbuchung>, ErrorOnRequest> {
    let url = einzelbuchungen_route(server_configuration);
    let request = get_request(url, login_credentials).await?;
    let result_dtos = serde_json::from_str::<Vec<EinzelbuchungDto>>(&request).unwrap();
    println!("Result dto {:?}", result_dtos);
    let result = map_einzelbuchungen(result_dtos);
    println!("Result as entity {:?}", result);
    Ok(result)
}

#[derive(Deserialize, Debug)]
pub struct EinzelbuchungDto {
    pub datum: String,
    pub name: String,
    pub kategorie: String,
    pub wert: String,
}

pub fn map_einzelbuchungen(dto: Vec<EinzelbuchungDto>) -> Vec<Einzelbuchung> {
    dto.into_iter().map(map_einzelbuchung).collect()
}

pub fn map_einzelbuchung(dto: EinzelbuchungDto) -> Einzelbuchung {
    Einzelbuchung {
        datum: Datum::from_iso_string(&dto.datum),
        name: Name::new(dto.name),
        kategorie: Kategorie::new(dto.kategorie),
        betrag: Betrag::from_iso_string(&dto.wert),
    }
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

        let local_server_name = LocalServerName {
            protocol: "http".to_string(),
            app_domain: "localhost".to_string(),
            app_port: 8080,
        };

        let result = request_login(&server_config, &local_server_name);

        assert_eq!(
            result.target,
            "MyServerUrl/offlinelogin?redirect=http://localhost:8080"
        )
    }
}
