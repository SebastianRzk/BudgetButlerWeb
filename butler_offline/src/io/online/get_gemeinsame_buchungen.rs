use crate::io::online::request::{get_request, ErrorOnRequest};
use crate::io::online::routes::gemeinsame_buchungen_route;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::person::Person;
use crate::model::remote::login::LoginCredentials;
use crate::model::remote::server::ServerConfiguration;
use crate::model::state::config::UserConfiguration;
use serde::Deserialize;

pub async fn request_gemeinsame_buchungen(
    server_configuration: &ServerConfiguration,
    user_configuration: &UserConfiguration,
    login_credentials: LoginCredentials,
) -> Result<Vec<GemeinsameBuchung>, ErrorOnRequest> {
    let url = gemeinsame_buchungen_route(server_configuration);
    let request = get_request(url, login_credentials.clone()).await?;
    let result_dtos = serde_json::from_str::<Vec<GemeinsamebuchungDto>>(&request).unwrap();
    println!("Result dto {:?}", result_dtos);
    let result = map_gemeinsame_buchungen(
        result_dtos,
        login_credentials.username.clone(),
        user_configuration.self_name.clone(),
        user_configuration.partner_name.clone(),
    );
    println!("Result as entity {:?}", result);
    Ok(result)
}

#[derive(Deserialize, Debug)]
pub struct GemeinsamebuchungDto {
    pub datum: String,
    pub name: String,
    pub kategorie: String,
    pub wert: String,
    pub zielperson: String,
}

pub fn map_gemeinsame_buchungen(
    dto: Vec<GemeinsamebuchungDto>,
    self_name_remote: String,
    self_name_local: Person,
    partner_name_local: Person,
) -> Vec<GemeinsameBuchung> {
    dto.into_iter()
        .map(|x| {
            map_gemeinsame_buchung(
                x,
                self_name_remote.clone(),
                self_name_local.clone(),
                partner_name_local.clone(),
            )
        })
        .collect()
}

pub fn map_gemeinsame_buchung(
    dto: GemeinsamebuchungDto,
    self_name_remote: String,
    self_name_local: Person,
    partner_name_local: Person,
) -> GemeinsameBuchung {
    println!("Mapping dto {:?}", dto);
    println!("self_name_remote {:?}", self_name_remote);
    println!("self_name_local {:?}", self_name_local);
    let person = if dto.zielperson == self_name_remote {
        self_name_local
    } else {
        partner_name_local
    };

    GemeinsameBuchung {
        datum: Datum::from_iso_string(&dto.datum),
        name: Name::new(dto.name),
        kategorie: Kategorie::new(dto.kategorie),
        betrag: Betrag::from_iso_string(&dto.wert),
        person,
    }
}

#[cfg(test)]
mod tests {
    use crate::io::online::get_gemeinsame_buchungen::{
        map_gemeinsame_buchung, GemeinsamebuchungDto,
    };
    use crate::model::primitives::person::builder::{demo_partner, demo_self};

    #[test]
    fn test_should_map_for_self() {
        let result = map_gemeinsame_buchung(
            GemeinsamebuchungDto {
                datum: "2021-01-01".to_string(),
                name: "ThisIsRemoteSelf".to_string(),
                kategorie: "Kategorie".to_string(),
                wert: "1.23".to_string(),
                zielperson: "ThisIsRemoteSelf".to_string(),
            },
            "ThisIsRemoteSelf".to_string(),
            demo_self(),
            demo_partner(),
        );

        assert_eq!(result.person, demo_self());
    }
    #[test]
    fn test_should_map_for_partner() {
        let result = map_gemeinsame_buchung(
            GemeinsamebuchungDto {
                datum: "2021-01-01".to_string(),
                name: "this is a partner".to_string(),
                kategorie: "Kategorie".to_string(),
                wert: "1.23".to_string(),
                zielperson: "partner".to_string(),
            },
            "ThisIsRemoteSelf".to_string(),
            demo_self(),
            demo_partner(),
        );

        assert_eq!(result.person, demo_partner());
    }
}
