use crate::model::state::non_persistent_application_state::StaticPathDirectory;
use actix_files::NamedFile;
use actix_web::http::header::{ContentDisposition, DispositionType};
use actix_web::web::Data;
use actix_web::{get, Error};
use std::path::PathBuf;

#[get("/static/{file_name}")]
async fn static_files(
    file_name: actix_web::web::Path<String>,
    static_path_directory: Data<StaticPathDirectory>,
) -> Result<NamedFile, Error> {
    let complete_path = to_static_path(&static_path_directory, file_name.into_inner().as_str());
    Ok(NamedFile::open(complete_path)?
        .use_last_modified(true)
        .set_content_disposition(ContentDisposition {
            disposition: DispositionType::Inline,
            parameters: vec![],
        }))
}

#[get("/fonts/{file_name}")]
async fn static_fonts(
    file_name: actix_web::web::Path<String>,
    static_path_directory: Data<StaticPathDirectory>,
) -> Result<NamedFile, Error> {
    let complete_path =
        to_static_font_path(&static_path_directory, file_name.into_inner().as_str());
    Ok(NamedFile::open(complete_path)?
        .use_last_modified(true)
        .set_content_disposition(ContentDisposition {
            disposition: DispositionType::Inline,
            parameters: vec![],
        }))
}

fn to_static_font_path(
    static_path_directory: &StaticPathDirectory,
    static_file_name: &str,
) -> PathBuf {
    to_static_path(static_path_directory, "fonts").join(static_file_name)
}

fn to_static_path(static_path_directory: &StaticPathDirectory, static_file_name: &str) -> PathBuf {
    static_path_directory.path.clone().join(static_file_name)
}
