use crate::budgetbutler::pages::sparen::uebersicht_etfs::{
    handle_uebersicht_etf, UebersichtEtfContext,
};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::budgetbutler::view::routes::SPAREN_UEBERSICHT_ETFS;
use crate::io::html::views::sparen::uebersicht_etfs::render_uebersicht_etf_template;
use crate::model::shares::ShareState;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("uebersicht_etfs/")]
pub async fn get_view(
    config: Data<ConfigurationData>,
    data: Data<ApplicationState>,
    shares: Data<ShareState>,
) -> impl Responder {
    let configuration_guard = config.configuration.lock().unwrap();

    let database = data.database.lock().unwrap();

    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht ETFs",
        SPAREN_UEBERSICHT_ETFS,
        UebersichtEtfContext {
            shares: &shares,
            database: &database,
        },
        handle_uebersicht_etf,
        render_uebersicht_etf_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}
