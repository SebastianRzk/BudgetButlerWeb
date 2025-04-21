use crate::budgetbutler::view::request_handler::{
    handle_render_success_display_message, ActivePage, DisplaySuccessMessage,
};
use crate::budgetbutler::view::routes::CORE_IMPORT;
use crate::io::http::shared::redirect_authenticated::{
    RedirectAuthenticatedRenderPageType, RedirectAuthenticatedResult,
};
use crate::io::online::begleiterapp::delete_kategorien::request_delete_kategorien;
use crate::io::online::begleiterapp::set_kategorien::request_set_kategorien;
use crate::model::remote::login::LoginCredentials;
use crate::model::state::config::Configuration;
use crate::model::state::persistent_application_state::Database;

pub async fn upload_kategorien(
    config: &Configuration,
    login: LoginCredentials,
    database: &Database,
) -> RedirectAuthenticatedResult {
    let kategorien = database.einzelbuchungen.get_kategorien();
    request_delete_kategorien(&config.server_configuration, login.clone())
        .await
        .expect("Failed to delete Kategorien");
    request_set_kategorien(&config.server_configuration, login, kategorien.clone())
        .await
        .expect("Failed to set Kategorien");

    let database_name = config.database_configuration.name.clone();
    let context = DisplaySuccessMessage {
        message: format!(
            "Erfolgreich {} Kategorien in die Online-App importiert",
            kategorien.len()
        ),
        link_name: "Zurück zu Import / Export".to_string(),
        link_url: CORE_IMPORT.to_string(),
    };
    RedirectAuthenticatedResult {
        database_to_save: None,
        page_render_type: RedirectAuthenticatedRenderPageType::RenderPage(
            handle_render_success_display_message(
                "Import von Einzelbuchungen",
                ActivePage::construct_from_url(CORE_IMPORT),
                database_name,
                context,
            ),
        ),
    }
}
