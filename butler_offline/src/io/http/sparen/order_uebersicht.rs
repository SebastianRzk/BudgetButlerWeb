use crate::budgetbutler::pages::sparen::uebersicht_order::{handle_view, UebersichtOrderContext};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, ActivePage};
use crate::budgetbutler::view::routes::SPAREN_ORDER_UEBERSICHT;
use crate::io::html::views::index::PageTitle;
use crate::io::html::views::sparen::uebersicht_order::render_uebersicht_order_template;
use crate::io::time::today;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("uebersicht_order/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    configuration_data: Data<ConfigurationData>,
) -> impl Responder {
    let database = data.database.lock().unwrap();
    let context = UebersichtOrderContext {
        database: &database,
        today: today(),
        angefordertes_jahr: None,
    };
    let database_name = configuration_data
        .configuration
        .lock()
        .unwrap()
        .database_configuration
        .name
        .clone();
    let active_page = ActivePage::construct_from_url(SPAREN_ORDER_UEBERSICHT);
    let view_result = handle_view(context);
    let render_view = render_uebersicht_order_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Übersicht Order"),
        active_page,
        database_name,
        render_view,
    ))
}

#[derive(Deserialize)]
struct FormData {
    date: i32,
}

#[post("uebersicht_order/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    form: Form<FormData>,
    configuration_data: Data<ConfigurationData>,
) -> impl Responder {
    let database = data.database.lock().unwrap();
    let context = UebersichtOrderContext {
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
    let active_page = ActivePage::construct_from_url(SPAREN_ORDER_UEBERSICHT);
    let view_result = handle_view(context);
    let render_view = render_uebersicht_order_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Übersicht Order"),
        active_page,
        database_name,
        render_view,
    ))
}
