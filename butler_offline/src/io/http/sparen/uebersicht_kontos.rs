use crate::budgetbutler::pages::sparen::uebersicht_kontos::{
    handle_uebersicht_kontos, UebersichtKontosContext,
};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, ActivePage};
use crate::budgetbutler::view::routes::SPAREN_SPARKONTO_UEBERSICHT;
use crate::io::html::views::index::PageTitle;
use crate::io::html::views::sparen::uebersicht_kontos::render_uebersicht_kontos_template;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("uebersicht_sparkontos/")]
pub async fn get_view(
    config: Data<ConfigurationData>,
    data: Data<ApplicationState>,
) -> impl Responder {
    let configuration_guard = config.configuration.lock().unwrap();

    let database = data.database.lock().unwrap();

    let context = UebersichtKontosContext {
        database: &database,
    };
    let database_name = configuration_guard.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url(SPAREN_SPARKONTO_UEBERSICHT);
    let view_result = handle_uebersicht_kontos(context);
    let render_view = render_uebersicht_kontos_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Übersicht Sparkontos"),
        active_page,
        database_name,
        render_view,
    ))
}
