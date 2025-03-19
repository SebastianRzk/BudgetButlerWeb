use crate::budgetbutler::pages::sparen::uebersicht_order_dauerauftraege::{
    handle_view, UebersichtOrderDauerauftraegeContext,
};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, ActivePage};
use crate::budgetbutler::view::routes::SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT;
use crate::io::html::views::index::PageTitle;
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
    let context = UebersichtOrderDauerauftraegeContext {
        database: &database,
        today: today(),
    };
    let database_name = config.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url(SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT);
    let view_result = handle_view(context);
    let render_view = render_uebersicht_order_dauerauftraege_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Übersicht Order-Daueraufträge"),
        active_page,
        database_name,
        render_view,
    ))
}
