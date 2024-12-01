use crate::budgetbutler::pages::core::error_optimistic_locking::{handle_optimistic_locking_error, ErrorOptimisticLockingContext};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::io::html::views::core::error_optimistic_locking::render_error_optimistic_locking_template;
use actix_web::{get, HttpResponse, Responder};

#[get("/error-optimistic-locking")]
pub async fn error_optimistic_locking() -> impl Responder {
    HttpResponse::Ok().body(
        handle_render_display_view("Error Veralteter Datenbestand",
                                   "/",
                                   ErrorOptimisticLockingContext{
                                   },
                                   handle_optimistic_locking_error,
                                   render_error_optimistic_locking_template))
}

