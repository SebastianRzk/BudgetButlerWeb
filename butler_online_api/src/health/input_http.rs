use actix_web::body::BoxBody;
use actix_web::{get, HttpResponse, Responder};

#[get("/health")]
pub async fn health_status() -> actix_web::Result<impl Responder> {
    Ok(HttpResponse::Created().body(BoxBody::new("UP")))
}
