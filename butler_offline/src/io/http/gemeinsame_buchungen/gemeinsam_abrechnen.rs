use crate::budgetbutler::pages::gemeinsame_buchungen::gemeinsam_abrechnen::{
    handle_view, GemeinsameBuchungenAbrechnenContext, Limit,
};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::budgetbutler::view::routes::GEMEINSAME_BUCHUNGEN_ABRECHNEN;
use crate::io::html::views::gemeinsame_buchungen::gemeinsame_buchungen_abrechnen::render_gemeinsame_buchungen_abrechnen;
use crate::io::time::today;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::person::Person;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::AdditionalKategorie;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("gemeinsamabrechnen/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    extra_kategorie: Data<AdditionalKategorie>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Gemeinsame Buchungen Abrechnen",
        GEMEINSAME_BUCHUNGEN_ABRECHNEN,
        GemeinsameBuchungenAbrechnenContext {
            extra_kategorie: &extra_kategorie.kategorie.lock().unwrap(),
            configuration: configuration_guard.clone(),
            today: today(),
            database: &database_guard,
            set_mindate: None,
            set_maxdate: None,
            set_verhaeltnis: None,
            set_limit: None,
            set_titel: None,
            set_other_kategorie: Kategorie::new("Unbekannt".to_string()),
            set_self_kategorie: Kategorie::new("Unbekannt".to_string()),
        },
        handle_view,
        render_gemeinsame_buchungen_abrechnen,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[post("gemeinsamabrechnen/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    extra_kategorie: Data<AdditionalKategorie>,
    config: Data<ConfigurationData>,
    form: Form<FormData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Gemeinsame Buchungen Abrechnen",
        GEMEINSAME_BUCHUNGEN_ABRECHNEN,
        GemeinsameBuchungenAbrechnenContext {
            extra_kategorie: &extra_kategorie.kategorie.lock().unwrap(),
            configuration: configuration_guard.clone(),
            today: today(),
            database: &database_guard,
            set_mindate: Some(Datum::from_iso_string(&form.set_mindate)),
            set_maxdate: Some(Datum::from_iso_string(&form.set_maxdate)),
            set_titel: Some(form.set_titel.clone()),
            set_verhaeltnis: form.set_verhaeltnis.parse().ok(),
            set_limit: map_get_limit(
                form.set_limit.clone(),
                form.set_limit_value.clone(),
                form.set_limit_fuer.clone(),
            ),
            set_other_kategorie: Kategorie::new(form.set_other_kategorie_value.clone()),
            set_self_kategorie: Kategorie::new(form.set_self_kategorie_value.clone()),
        },
        handle_view,
        render_gemeinsame_buchungen_abrechnen,
        configuration_guard.database_configuration.name.clone(),
    ))
}

fn map_get_limit(
    filter: Option<String>,
    filter_value: Option<String>,
    filter_person: Option<String>,
) -> Option<Limit> {
    if let Some(filter) = filter {
        if filter == "on".to_string() {
            return Some(Limit {
                fuer: Person::new(filter_person.unwrap()),
                value: Betrag::from_user_input(&filter_value.unwrap()).negativ(),
            });
        }
    }
    None
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
