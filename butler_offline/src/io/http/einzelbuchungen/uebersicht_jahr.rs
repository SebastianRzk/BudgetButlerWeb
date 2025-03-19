use crate::budgetbutler::pages::einzelbuchungen::uebersicht_jahr::{
    handle_view, UebersichtJahrContext,
};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, ActivePage};
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_JAHRESUEBERSICHT;
use crate::io::html::views::einzelbuchungen::uebersicht_jahr::render_uebersicht_jahr_template;
use crate::io::html::views::index::PageTitle;
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
    let context = UebersichtJahrContext {
        database: &database_guard,
        angefordertes_jahr: None,
        konfigurierte_farben: configuration_guard
            .design_configuration
            .configurierte_farben
            .clone(),
        today: today(),
    };
    let database_name = configuration_guard.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url(EINZELBUCHUNGEN_JAHRESUEBERSICHT);
    let view_result = handle_view(context);
    let render_view = render_uebersicht_jahr_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Jahresübersicht"),
        active_page,
        database_name,
        render_view,
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
    let context = UebersichtJahrContext {
        database: &database_guard,
        angefordertes_jahr: Some(jahr),
        konfigurierte_farben: configuration_guard
            .design_configuration
            .configurierte_farben
            .clone(),
        today: today(),
    };
    let database_name = configuration_guard.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url(EINZELBUCHUNGEN_JAHRESUEBERSICHT);
    let view_result = handle_view(context);
    let render_view = render_uebersicht_jahr_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Jahresübersicht"),
        active_page,
        database_name,
        render_view,
    ))
}
