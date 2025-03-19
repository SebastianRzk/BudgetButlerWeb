use crate::budgetbutler::pages::gemeinsame_buchungen::uebersicht_abrechnungen::{
    handle_view_abrechnungen, UebersichtAbrechnugnenContext,
};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, ActivePage};
use crate::budgetbutler::view::routes::GEMEINSAME_BUCHUNGEN_ABRECHNUNGEN;
use crate::io::disk::abrechnung::history::lade_alle_abrechnungen;
use crate::io::html::views::gemeinsame_buchungen::uebersicht_abrechnungen::render_uebersicht_gemeinsame_abrechnungen_template;
use crate::io::html::views::index::PageTitle;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};
use serde::Deserialize;

#[get("uebersichtabrechnungen/")]
pub async fn get_view(
    config: Data<ConfigurationData>,
    user_application_directory: Data<UserApplicationDirectory>,
) -> impl Responder {
    let configuration_guard = config.configuration.lock().unwrap();
    let alle_abrechnung = lade_alle_abrechnungen(
        &user_application_directory,
        &configuration_guard.abrechnungs_configuration,
    );
    let context = UebersichtAbrechnugnenContext {
        abrechnungen: alle_abrechnung,
    };
    let database_name = configuration_guard.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url(GEMEINSAME_BUCHUNGEN_ABRECHNUNGEN);
    let view_result = handle_view_abrechnungen(context);
    let render_view = render_uebersicht_gemeinsame_abrechnungen_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Übersicht Abrechnungen"),
        active_page,
        database_name,
        render_view,
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
