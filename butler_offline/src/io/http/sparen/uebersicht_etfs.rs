use crate::budgetbutler::pages::sparen::uebersicht_etfs::{
    handle_uebersicht_etf, UebersichtEtfContext,
};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, ActivePage};
use crate::budgetbutler::view::routes::SPAREN_UEBERSICHT_ETFS;
use crate::io::html::views::index::PageTitle;
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

    let context = UebersichtEtfContext {
        shares: &shares,
        database: &database,
    };
    let database_name = configuration_guard.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url(SPAREN_UEBERSICHT_ETFS);
    let view_result = handle_uebersicht_etf(context);
    let render_view = render_uebersicht_etf_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Übersicht ETFs"),
        active_page,
        database_name,
        render_view,
    ))
}
