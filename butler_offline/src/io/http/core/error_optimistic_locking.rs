use crate::budgetbutler::view::request_handler::{handle_render_display_view, no_page_middleware};
use crate::io::html::views::core::error_optimistic_locking::render_error_optimistic_locking_template;
use crate::model::state::config::ConfigurationData;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("/error-optimistic-locking")]
pub async fn error_optimistic_locking(configuration: Data<ConfigurationData>) -> impl Responder {
    HttpResponse::Ok().body(handle_render_display_view(
        "Error Veralteter Datenbestand",
        "/",
        None,
        no_page_middleware,
        render_error_optimistic_locking_template,
        configuration
            .configuration
            .lock()
            .unwrap()
            .database_configuration
            .name
            .clone(),
    ))
}
