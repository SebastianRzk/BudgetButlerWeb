use crate::budgetbutler::pages::gemeinsame_buchungen::uebersicht_gemeinsame_buchungen::{
    handle_view, UebersichtGemeinsameBuchungenContext,
};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::budgetbutler::view::routes::GEMEINSAME_BUCHUNGEN_UEBERSICHT;
use crate::io::html::views::gemeinsame_buchungen::uebersicht_gemeinsame_buchungen::render_uebersicht_gemeinsame_buchungen_template;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("gemeinsameuebersicht/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    configuration_data: Data<ConfigurationData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let config = configuration_data.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Gemeinsame Buchungen",
        GEMEINSAME_BUCHUNGEN_UEBERSICHT,
        UebersichtGemeinsameBuchungenContext {
            database: &database_guard,
        },
        handle_view,
        render_uebersicht_gemeinsame_buchungen_template,
        config.database_configuration.name.clone(),
    ))
}
