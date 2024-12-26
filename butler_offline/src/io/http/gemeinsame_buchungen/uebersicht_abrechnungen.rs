use crate::budgetbutler::pages::gemeinsame_buchungen::uebersicht_abrechnungen::{
    handle_view_abrechnungen, UebersichtAbrechnugnenContext,
};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::budgetbutler::view::routes::GEMEINSAME_BUCHUNGEN_ABRECHNUNGEN;
use crate::io::disk::abrechnung::history::lade_alle_abrechnungen;
use crate::io::html::views::gemeinsame_buchungen::uebersicht_abrechnungen::render_uebersicht_gemeinsame_abrechnungen_template;
use crate::model::state::config::ConfigurationData;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};
use serde::Deserialize;

#[get("uebersichtabrechnungen/")]
pub async fn get_view(config: Data<ConfigurationData>) -> impl Responder {
    let configuration_guard = config.configuration.lock().unwrap();
    let alle_abrechnung = lade_alle_abrechnungen(&configuration_guard.abrechnungs_configuration);
    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht Abrechnungen",
        GEMEINSAME_BUCHUNGEN_ABRECHNUNGEN,
        UebersichtAbrechnugnenContext {
            abrechnungen: alle_abrechnung,
        },
        handle_view_abrechnungen,
        render_uebersicht_gemeinsame_abrechnungen_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[derive(Deserialize)]
pub struct FormData {
    pub set_mindate: String,
    pub set_maxdate: String,
    pub set_verhaeltnis: String,
    pub set_titel: String,

    pub set_limit: Option<String>,
    pub set_limit_fuer: Option<String>,
    pub set_limit_value: Option<String>,

    pub set_self_kategorie_value: String,
    pub set_other_kategorie_value: String,
}
