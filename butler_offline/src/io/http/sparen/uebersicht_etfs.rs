use crate::budgetbutler::pages::sparen::uebersicht_etfs::{
    handle_uebersicht_etf, UebersichtEtfContext,
};
use crate::budgetbutler::view::menu::resolve_active_group_from_url;
use crate::budgetbutler::view::request_handler::{ActivePage, SuccessMessage};
use crate::budgetbutler::view::routes::SPAREN_UEBERSICHT_ETFS;
use crate::io::html::views::index::{render_index_template, PageTitle};
use crate::io::html::views::sparen::uebersicht_etfs::render_uebersicht_etf_template;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use crate::model::state::shares::SharesData;
use actix_web::web::{Data, Query};
use actix_web::{get, HttpResponse, Responder};
use serde::Deserialize;

#[derive(Deserialize)]
struct OptionalMessageQueryParam {
    pub message: Option<String>,
}

#[get("uebersicht_etfs/")]
pub async fn get_view(
    config: Data<ConfigurationData>,
    data: Data<ApplicationState>,
    shares: Data<SharesData>,
    message: Query<OptionalMessageQueryParam>,
) -> impl Responder {
    let configuration_guard = config.configuration.lock().unwrap();

    let database = data.database.lock().unwrap();

    let context = UebersichtEtfContext {
        shares: &shares.data.lock().unwrap(),
        database: &database,
    };
    let database_name = configuration_guard.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url(SPAREN_UEBERSICHT_ETFS);
    let view_result = handle_uebersicht_etf(context);
    let render_view = render_uebersicht_etf_template(view_result);
    HttpResponse::Ok().body(render_index_template(
        resolve_active_group_from_url(&active_page),
        active_page,
        PageTitle::new("Depot Analyse"),
        render_view,
        message
            .message
            .clone()
            .map(|x| SuccessMessage { message: x.clone() })
            .or(None),
        database_name,
    ))
}
