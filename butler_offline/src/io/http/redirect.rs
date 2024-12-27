use crate::budgetbutler::view::request_handler;
use actix_web::HttpResponse;

pub fn http_redirect(redirect: request_handler::Redirect) -> HttpResponse {
    HttpResponse::SeeOther()
        .append_header(("Location", redirect.target))
        .finish()
}
