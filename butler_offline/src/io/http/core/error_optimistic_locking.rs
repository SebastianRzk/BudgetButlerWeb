use crate::budgetbutler::view::request_handler::{
    handle_render_display_view, no_page_middleware, ActivePage,
};
use crate::io::html::views::core::error_optimistic_locking::render_error_optimistic_locking_template;
use crate::io::html::views::index::PageTitle;
use crate::model::state::config::ConfigurationData;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("/error-optimistic-locking")]
pub async fn error_optimistic_locking(configuration: Data<ConfigurationData>) -> impl Responder {
    let database_name = configuration
        .configuration
        .lock()
        .unwrap()
        .database_configuration
        .name
        .clone();
    let active_page = ActivePage::construct_from_url("/");
    let view_result = no_page_middleware(None);
    let render_view = render_error_optimistic_locking_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Error Veralteter Datenbestand"),
        active_page,
        database_name,
        render_view,
    ))
}
