use crate::model::state::config::ConfigurationData;
use actix_web::http::header::{CacheControl, CacheDirective, ContentType};
use actix_web::web::Data;
use actix_web::{get, HttpResponse};

const THEME: &str = include_str!("../../../templates/theme.css");

#[get("/theme/")]
pub async fn get_css_theme(config: Data<ConfigurationData>) -> HttpResponse {
    let css_text = THEME.replace(
        "{THEME_COLOR}",
        config
            .configuration
            .lock()
            .unwrap()
            .design_configuration
            .design_farbe
            .as_string
            .as_str(),
    );
    HttpResponse::Ok()
        .insert_header(ContentType(mime::TEXT_CSS))
        .insert_header(CacheControl(vec![CacheDirective::NoCache]))
        .body(css_text)
}
