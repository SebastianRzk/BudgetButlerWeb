use crate::budgetbutler::pages::sparen::uebersicht_kontos::{
    handle_uebersicht_kontos, UebersichtKontosContext,
};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::budgetbutler::view::routes::SPAREN_SPARKONTO_UEBERSICHT;
use crate::io::html::views::sparen::uebersicht_kontos::render_uebersicht_kontos_template;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("uebersicht_sparkontos/")]
pub async fn get_view(
    config: Data<ConfigurationData>,
    data: Data<ApplicationState>,
) -> impl Responder {
    let configuration_guard = config.configuration.lock().unwrap();

    let database = data.database.lock().unwrap();

    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Sparkontos",
        SPAREN_SPARKONTO_UEBERSICHT,
        UebersichtKontosContext {
            database: &database,
        },
        handle_uebersicht_kontos,
        render_uebersicht_kontos_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}
