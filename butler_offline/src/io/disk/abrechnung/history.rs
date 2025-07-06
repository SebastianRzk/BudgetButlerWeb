use crate::budgetbutler::database::abrechnen::persoenliche_buchungen_abrechnen::history::UnparsedAbrechnungsFile;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::state::config::AbrechnungsConfiguration;
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;

pub fn lade_alle_abrechnungen(
    user_application_directory: &UserApplicationDirectory,
    config: &AbrechnungsConfiguration,
) -> Vec<UnparsedAbrechnungsFile> {
    let mut result = vec![];
    let path = user_application_directory
        .path
        .join(std::path::Path::new(&config.location));
    eprintln!("Lade Abrechnungen aus: {path:?}");

    for file in std::fs::read_dir(path).unwrap() {
        let file = file.unwrap();
        let file_path = file.path();
        let file_size = file.metadata().unwrap().len();
        if file_size == 0
            || file_size > 10 * 1024 * 1024
            || file.file_type().unwrap().is_dir()
            || file_path.extension().unwrap_or("".as_ref()) != "txt"
        {
            continue;
        }

        let file_name = file_path.file_name().unwrap().to_str().unwrap().to_string();
        let file_content = std::fs::read_to_string(file_path).unwrap();
        result.push(UnparsedAbrechnungsFile {
            file_name,
            file_content: Line::from_multiline_str(file_content),
        });
    }

    result
}
