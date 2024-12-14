use crate::io::online::request::{post_request, ErrorOnRequest};
use crate::io::online::routes::gemeinsame_buchungen_batch_route;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::primitives::person::Person;
use crate::model::remote::login::LoginCredentials;
use crate::model::remote::server::ServerConfiguration;
use crate::model::state::config::UserConfiguration;
use serde::Serialize;

pub async fn put_gemeinsame_buchungen(
    server_configuration: &ServerConfiguration,
    user_configuration: &UserConfiguration,
    login_credentials: LoginCredentials,
    gemeinsame_buchungen: Vec<GemeinsameBuchung>,
) -> Result<(), ErrorOnRequest> {
    let url = gemeinsame_buchungen_batch_route(server_configuration);
    let gemeinsame_buchungen_dtos =
        map_gemeinsame_buchungen(gemeinsame_buchungen, user_configuration.self_name.clone());
    let request_str = serde_json::to_string(&gemeinsame_buchungen_dtos).unwrap();
    println!("Result dto {:?}", request_str);
    post_request(url, login_credentials.clone(), request_str).await?;
    Ok(())
}

#[derive(Serialize, Debug)]
#[serde(rename_all = "camelCase")]
pub struct GemeinsameBuchungDto {
    pub datum: String,
    pub name: String,
    pub kategorie: String,
    pub wert: String,
    pub eigene_buchung: bool,
}

pub fn map_gemeinsame_buchungen(
    dto: Vec<GemeinsameBuchung>,
    self_name_local: Person,
) -> Vec<GemeinsameBuchungDto> {
    dto.into_iter()
        .map(|x| map_gemeinsame_buchung(x, self_name_local.clone()))
        .collect()
}

pub fn map_gemeinsame_buchung(
    entity: GemeinsameBuchung,
    self_name_local: Person,
) -> GemeinsameBuchungDto {
    GemeinsameBuchungDto {
        datum: entity.datum.to_iso_string(),
        name: entity.name.get_name().clone(),
        kategorie: entity.kategorie.kategorie,
        wert: entity.betrag.to_iso_string(),
        eigene_buchung: entity.person == self_name_local,
    }
}

#[cfg(test)]
mod tests {
    use crate::io::online::put_gemeinsame_buchungen::map_gemeinsame_buchung;
    use crate::model::database::gemeinsame_buchung::builder::gemeinsame_buchung_mit_person;
    use crate::model::primitives::person::builder::person;

    #[test]
    fn test_should_map_for_self() {
        let result = map_gemeinsame_buchung(
            gemeinsame_buchung_mit_person("ThisIsSelf"),
            person("ThisIsSelf"),
        );

        assert_eq!(result.eigene_buchung, true);
    }
    #[test]
    fn test_should_map_for_partner() {
        let result = map_gemeinsame_buchung(
            gemeinsame_buchung_mit_person("ThisIsNotSelf"),
            person("ThisIsSelf"),
        );

        assert_eq!(result.eigene_buchung, false);
    }
}
