use actix_web::http::header::ContentType;
use actix_web::{get, HttpResponse};
use actix_web::web::Data;
use crate::model::state::config::Config;

const THEME: &str = include_str!("../../../templates/theme.css");

#[get("/theme/")]
pub async fn get_css_theme(config: Data<Config>) -> HttpResponse {
    let css_text = THEME.replace("{THEME_COLOR}", config.design_configuration.design_farbe.as_string.as_str());
    HttpResponse::Ok().insert_header(ContentType(mime::TEXT_CSS)).body(css_text)
}

