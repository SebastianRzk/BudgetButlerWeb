use crate::budgetbutler::pages::sparen::uebersicht_order_dauerauftraege::{
    handle_view, UebersichtOrderDauerauftraegeContext,
};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::budgetbutler::view::routes::SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT;
use crate::io::html::views::sparen::uebersicht_order_dauerauftraege::render_uebersicht_order_dauerauftraege_template;
use crate::io::time::today;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("uebersicht_orderdauerauftrag/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let database = data.database.lock().unwrap();
    let config = configuration.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Order-Daueraufträge",
        SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT,
        UebersichtOrderDauerauftraegeContext {
            database: &database,
            today: today(),
        },
        handle_view,
        render_uebersicht_order_dauerauftraege_template,
        config.database_configuration.name.clone(),
    ))
}
