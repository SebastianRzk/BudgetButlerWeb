use crate::budgetbutler::pages::sparen::uebersicht_depotauszuege::{
    handle_uebersicht_depotauszuege, UebersichtDepotauszuegeContext,
};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, ActivePage};
use crate::budgetbutler::view::routes::SPAREN_DEPOTAUSZUEGE_UEBERSICHT;
use crate::io::html::views::index::PageTitle;
use crate::io::html::views::sparen::uebersicht_depotauszuege::render_uebersicht_depotauszuege_template;
use crate::io::time::today;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("uebersicht_depotauszuege/")]
pub async fn get_view(
    config: Data<ConfigurationData>,
    data: Data<ApplicationState>,
) -> impl Responder {
    let configuration_guard = config.configuration.lock().unwrap();

    let database = data.database.lock().unwrap();

    let context = UebersichtDepotauszuegeContext {
        today: today(),
        angefordertes_jahr: None,
        database: &database,
    };
    let database_name = configuration_guard.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url(SPAREN_DEPOTAUSZUEGE_UEBERSICHT);
    let view_result = handle_uebersicht_depotauszuege(context);
    let render_view = render_uebersicht_depotauszuege_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Übersicht Depotauszuege"),
        active_page,
        database_name,
        render_view,
    ))
}

#[post("uebersicht_depotauszuege/")]
pub async fn post_view(
    config: Data<ConfigurationData>,
    data: Data<ApplicationState>,
    form_data: Form<FormData>,
) -> impl Responder {
    let configuration_guard = config.configuration.lock().unwrap();

    let database = data.database.lock().unwrap();

    let context = UebersichtDepotauszuegeContext {
        database: &database,
        today: today(),
        angefordertes_jahr: Some(form_data.date),
    };
    let database_name = configuration_guard.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url(SPAREN_DEPOTAUSZUEGE_UEBERSICHT);
    let view_result = handle_uebersicht_depotauszuege(context);
    let render_view = render_uebersicht_depotauszuege_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Übersicht Depotauszuege"),
        active_page,
        database_name,
        render_view,
    ))
}

#[derive(Deserialize)]
struct FormData {
    date: i32,
}
