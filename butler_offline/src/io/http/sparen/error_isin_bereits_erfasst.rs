use crate::budgetbutler::view::request_handler::{
    handle_render_display_view, no_page_middleware, ActivePage,
};
use crate::io::html::views::index::PageTitle;
use crate::io::html::views::sparen::error_isin_bereits_erfasst::render_error_isin_bereits_erfasst_template;
use crate::model::state::config::ConfigurationData;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("/error-isin-bereits-erfasst")]
pub async fn error_isin_bereits_erfasst(configuration: Data<ConfigurationData>) -> impl Responder {
    let database_name = configuration
        .configuration
        .lock()
        .unwrap()
        .database_configuration
        .name
        .clone();
    let active_page = ActivePage::construct_from_url("/");
    let view_result = no_page_middleware(None);
    let render_view = render_error_isin_bereits_erfasst_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Error ISIN bereits erfasst"),
        active_page,
        database_name,
        render_view,
    ))
}
