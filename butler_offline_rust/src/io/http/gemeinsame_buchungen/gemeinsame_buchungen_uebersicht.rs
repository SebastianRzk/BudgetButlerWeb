use crate::budgetbutler::pages::gemeinsame_buchungen::uebersicht_gemeinsame_buchungen::{handle_view, UebersichtGemeinsameBuchungenContext};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::budgetbutler::view::routes::GEMEINSAME_BUCHUNGEN_UEBERSICHT;
use crate::io::html::views::gemeinsame_buchungen::uebersicht_gemeinsame_buchungen::render_uebersicht_gemeinsame_buchungen_template;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("gemeinsameuebersicht/")]
pub async fn get_view(data: Data<ApplicationState>) -> impl Responder {
    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Gemeinsame Buchungen",
        GEMEINSAME_BUCHUNGEN_UEBERSICHT,
        UebersichtGemeinsameBuchungenContext {
            database: &data.database.lock().unwrap(),
        },
        handle_view,
        render_uebersicht_gemeinsame_buchungen_template))
}


