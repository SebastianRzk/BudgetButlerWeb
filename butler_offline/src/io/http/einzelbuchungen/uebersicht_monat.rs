use crate::budgetbutler::pages::einzelbuchungen::uebersicht_monat::{
    handle_view, UebersichtMonatContext,
};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_MONATSUEBERSICHT;
use crate::io::html::views::einzelbuchungen::uebersicht_monat::render_uebersicht_monat_template;
use crate::io::time::today;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("monatsuebersicht/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Monat",
        EINZELBUCHUNGEN_MONATSUEBERSICHT,
        UebersichtMonatContext {
            database: &database_guard,
            angefordertes_jahr: None,
            angeforderter_monat: None,
            konfigurierte_farben: configuration_guard
                .design_configuration
                .configurierte_farben
                .clone(),
            today: today(),
        },
        handle_view,
        render_uebersicht_monat_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[derive(Deserialize)]
struct FormData {
    monat: String,
}

#[post("monatsuebersicht/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    form: Form<FormData>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let input = form.monat.split("-").collect::<Vec<&str>>();
    let jahr = input[0].parse::<i32>().unwrap();
    let monat = input[1].parse::<u32>().unwrap();

    let database_guard = data.database.lock().unwrap();
    let configuration_guard = config.configuration.lock().unwrap();

    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Monat",
        EINZELBUCHUNGEN_MONATSUEBERSICHT,
        UebersichtMonatContext {
            database: &database_guard,
            angefordertes_jahr: Some(jahr),
            angeforderter_monat: Some(monat),
            konfigurierte_farben: configuration_guard
                .design_configuration
                .configurierte_farben
                .clone(),
            today: today(),
        },
        handle_view,
        render_uebersicht_monat_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}
