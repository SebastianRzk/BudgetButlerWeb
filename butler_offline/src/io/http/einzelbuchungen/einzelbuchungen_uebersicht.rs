use crate::budgetbutler::pages::einzelbuchungen::uebersicht_einzelbuchungen::{
    handle_view, UebersichtEinzelbuchungenContext,
};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, ActivePage};
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT;
use crate::io::html::views::einzelbuchungen::uebersicht_einzelbuchungen::render_uebersicht_einzelbuchungen_template;
use crate::io::html::views::index::PageTitle;
use crate::io::time::today;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form, Query};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[derive(Deserialize)]
pub struct GetUebersichtEinzelbuchungenQuery {
    pub jahr: Option<i32>,
}

#[get("uebersicht/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    configuration_data: Data<ConfigurationData>,
    param: Query<GetUebersichtEinzelbuchungenQuery>,
) -> impl Responder {
    let database = data.database.lock().unwrap();
    let context = UebersichtEinzelbuchungenContext {
        database: &database,
        today: today(),
        angefordertes_jahr: param.jahr,
    };
    let database_name = configuration_data
        .configuration
        .lock()
        .unwrap()
        .database_configuration
        .name
        .clone();
    let active_page = ActivePage::construct_from_url(EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT);
    let view_result = handle_view(context);
    let render_view = render_uebersicht_einzelbuchungen_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Übersicht Einzelbuchungen"),
        active_page,
        database_name,
        render_view,
    ))
}

#[derive(Deserialize)]
struct FormData {
    date: i32,
}

#[post("uebersicht/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    form: Form<FormData>,
    configuration_data: Data<ConfigurationData>,
) -> impl Responder {
    let database = data.database.lock().unwrap();
    let context = UebersichtEinzelbuchungenContext {
        database: &database,
        today: today(),
        angefordertes_jahr: Some(form.date),
    };
    let database_name = configuration_data
        .configuration
        .lock()
        .unwrap()
        .database_configuration
        .name
        .clone();
    let active_page = ActivePage::construct_from_url(EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT);
    let view_result = handle_view(context);
    let render_view = render_uebersicht_einzelbuchungen_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Übersicht Einzelbuchungen"),
        active_page,
        database_name,
        render_view,
    ))
}
