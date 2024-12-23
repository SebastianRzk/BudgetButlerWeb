use crate::budgetbutler::view::request_handler::{handle_render_display_view, no_page_middleware};
use crate::io::html::views::core::error_keine_aktion_gefunden::render_error_keine_aktion_gefunden_template;
use crate::model::state::config::ConfigurationData;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("/error-keine-aktion-gefunden")]
pub async fn error_keine_aktion_gefunden(configuration: Data<ConfigurationData>) -> impl Responder {
    HttpResponse::Ok().body(handle_render_display_view(
        "Keine Aktion gefunden",
        "/",
        None,
        no_page_middleware,
        render_error_keine_aktion_gefunden_template,
        configuration
            .configuration
            .lock()
            .unwrap()
            .database_configuration
            .name
            .clone(),
    ))
}
