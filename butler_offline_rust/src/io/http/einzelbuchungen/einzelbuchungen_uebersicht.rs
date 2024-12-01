use crate::budgetbutler::pages::einzelbuchungen::uebersicht_einzelbuchungen::{handle_view, UebersichtEinzelbuchungenContext};
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT;
use crate::io::html::views::einzelbuchungen::uebersicht_einzelbuchungen::render_uebersicht_einzelbuchungen_template;
use crate::io::time::today;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;
use crate::budgetbutler::view::request_handler::handle_render_display_view;

#[get("uebersicht/")]
pub async fn get_view(data: Data<ApplicationState>) -> impl Responder {
    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Einzelbuchungen",
        EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT,
        UebersichtEinzelbuchungenContext {
            database: &data.database.lock().unwrap(),
            today: today(),
            angefordertes_jahr: None,
        },
        handle_view,
        render_uebersicht_einzelbuchungen_template))
}

#[derive(Deserialize)]
struct FormData {
    date: i32,
}


#[post("uebersicht/")]
pub async fn post_view(data: Data<ApplicationState>, form: Form<FormData>) -> impl Responder {
    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Einzelbuchungen",
        EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT,
        UebersichtEinzelbuchungenContext {
            database: &data.database.lock().unwrap(),
            today: today(),
            angefordertes_jahr: Some(form.date),
        },
        handle_view,
        render_uebersicht_einzelbuchungen_template))
}
