use crate::budgetbutler::view::request_handler::{
    handle_render_success_display_message, ActivePage, DisplaySuccessMessage,
};
use crate::budgetbutler::view::routes::CORE_IMPORT;
use crate::io::http::shared::redirect_authenticated::{
    RedirectAuthenticatedRenderPageType, RedirectAuthenticatedResult,
};
use crate::io::online::begleiterapp::put_gemeinsame_buchungen::put_gemeinsame_buchungen;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::remote::login::LoginCredentials;
use crate::model::state::config::Configuration;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::gemeinsame_buchungen::GemeinsameBuchungen;

pub async fn export_gemeinsame_buchungen_request(
    config: &Configuration,
    login: LoginCredentials,
    database: &Database,
) -> RedirectAuthenticatedResult {
    let alle_gemeinsamen_buchungen: Vec<GemeinsameBuchung> = database
        .gemeinsame_buchungen
        .gemeinsame_buchungen
        .iter()
        .map(|gb| gb.value.clone())
        .collect();

    let alle_gemeinsamen_buchungen_anzahl = alle_gemeinsamen_buchungen.len();

    put_gemeinsame_buchungen(
        &config.server_configuration,
        &config.user_configuration,
        login,
        alle_gemeinsamen_buchungen,
    )
    .await
    .unwrap();

    let neue_datenbank = database.change_gemeinsame_buchungen(GemeinsameBuchungen {
        gemeinsame_buchungen: vec![],
    });

    let database_name = config.database_configuration.name.clone();
    let context = DisplaySuccessMessage {
        message: format!(
            "Erfolgreich {alle_gemeinsamen_buchungen_anzahl} gemeinsame Buchungen exportiert"
        ),
        link_name: "Zurück zu Import / Export".to_string(),
        link_url: CORE_IMPORT.to_string(),
    };
    RedirectAuthenticatedResult {
        database_to_save: Some(neue_datenbank),
        page_render_type: RedirectAuthenticatedRenderPageType::RenderPage(
            handle_render_success_display_message(
                "Export von gemeinsamen Buchungen",
                ActivePage::construct_from_url(CORE_IMPORT),
                database_name,
                context,
            ),
        ),
    }
}
