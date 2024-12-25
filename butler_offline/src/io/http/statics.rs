use actix_files::NamedFile;
use actix_web::http::header::{ContentDisposition, DispositionType};
use actix_web::{get, Error};
use std::path::{Path, PathBuf};

const STATIC_PATH: &str = "./static";

#[get("/static/{file_name}")]
async fn static_files(file_name: actix_web::web::Path<String>) -> Result<NamedFile, Error> {
    let complete_path = to_static_path(file_name.into_inner().as_str());
    Ok(NamedFile::open(complete_path)?
        .use_last_modified(true)
        .set_content_disposition(ContentDisposition {
            disposition: DispositionType::Inline,
            parameters: vec![],
        }))
}

#[get("/fonts/{file_name}")]
async fn static_fonts(file_name: actix_web::web::Path<String>) -> Result<NamedFile, Error> {
    let complete_path = to_static_font_path(file_name.into_inner().as_str());
    Ok(NamedFile::open(complete_path)?
        .use_last_modified(true)
        .set_content_disposition(ContentDisposition {
            disposition: DispositionType::Inline,
            parameters: vec![],
        }))
}

fn to_static_font_path(static_file_name: &str) -> PathBuf {
    to_static_path("fonts").join(static_file_name)
}

fn to_static_path(static_file_name: &str) -> PathBuf {
    Path::new(STATIC_PATH).join(static_file_name)
}
