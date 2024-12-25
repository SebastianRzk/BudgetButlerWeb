use crate::budgetbutler::pages::sparen::uebersicht_depotwerte::{
    handle_uebersicht_depotwerte, UebersichtDepotwerteContext,
};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::budgetbutler::view::routes::SPAREN_DEPOTWERTE_UEBERSICHT;
use crate::io::html::views::sparen::uebersicht_depotwerte::render_uebersicht_depotwerte_template;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("uebersicht_depotwerte/")]
pub async fn get_view(
    config: Data<ConfigurationData>,
    data: Data<ApplicationState>,
) -> impl Responder {
    let configuration_guard = config.configuration.lock().unwrap();

    let database = data.database.lock().unwrap();

    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Depotwerte",
        SPAREN_DEPOTWERTE_UEBERSICHT,
        UebersichtDepotwerteContext {
            database: &database,
        },
        handle_uebersicht_depotwerte,
        render_uebersicht_depotwerte_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}
