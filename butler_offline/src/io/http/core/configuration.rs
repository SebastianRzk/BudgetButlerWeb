use crate::budgetbutler::pages::core::configuration::{handle_view, ConfigurationContext};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::budgetbutler::view::routes::CORE_CONFIGURATION;
use crate::io::html::views::core::configuration::render_configuration_template;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::AdditionalKategorie;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("configuration/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    config: Data<ConfigurationData>,
    additional_kategorie: Data<AdditionalKategorie>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let config_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Einstellungen",
        CORE_CONFIGURATION,
        ConfigurationContext {
            database: &database_guard,
            config: &config_guard,
            extra_kategorie: additional_kategorie.kategorie.lock().unwrap().clone(),
        },
        handle_view,
        render_configuration_template,
        config_guard.database_configuration.name.clone(),
    ))
}
