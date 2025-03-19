use crate::budgetbutler::pages::core::configuration::{handle_view, ConfigurationContext};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, ActivePage};
use crate::budgetbutler::view::routes::CORE_CONFIGURATION;
use crate::io::html::views::core::configuration::render_configuration_template;
use crate::io::html::views::index::PageTitle;
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
    let context = ConfigurationContext {
        database: &database_guard,
        config: &config_guard,
        extra_kategorie: additional_kategorie.kategorie.lock().unwrap().clone(),
    };
    let database_name = config_guard.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url(CORE_CONFIGURATION);
    let view_result = handle_view(context);
    let render_view = render_configuration_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Einstellungen"),
        active_page,
        database_name,
        render_view,
    ))
}
