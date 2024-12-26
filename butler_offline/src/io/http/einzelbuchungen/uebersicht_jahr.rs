use crate::budgetbutler::pages::einzelbuchungen::uebersicht_jahr::{
    handle_view, UebersichtJahrContext,
};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_JAHRESUEBERSICHT;
use crate::io::html::views::einzelbuchungen::uebersicht_jahr::render_uebersicht_jahr_template;
use crate::io::time::today;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("jahresuebersicht/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Monat",
        EINZELBUCHUNGEN_JAHRESUEBERSICHT,
        UebersichtJahrContext {
            database: &database_guard,
            angefordertes_jahr: None,
            konfigurierte_farben: configuration_guard
                .design_configuration
                .configurierte_farben
                .clone(),
            today: today(),
        },
        handle_view,
        render_uebersicht_jahr_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[derive(Deserialize)]
struct FormData {
    jahr: String,
}

#[post("jahresuebersicht/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    form: Form<FormData>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let jahr: i32 = form.jahr.parse().unwrap();

    let database_guard = data.database.lock().unwrap();
    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Monat",
        EINZELBUCHUNGEN_JAHRESUEBERSICHT,
        UebersichtJahrContext {
            database: &database_guard,
            angefordertes_jahr: Some(jahr),
            konfigurierte_farben: configuration_guard
                .design_configuration
                .configurierte_farben
                .clone(),
            today: today(),
        },
        handle_view,
        render_uebersicht_jahr_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}
