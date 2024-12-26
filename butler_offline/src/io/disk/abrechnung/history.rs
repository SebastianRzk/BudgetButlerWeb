use crate::budgetbutler::database::abrechnen::abrechnen::history::UnparsedAbrechnungsFile;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::state::config::{app_root, AbrechnungsConfiguration};

pub fn lade_alle_abrechnungen(config: &AbrechnungsConfiguration) -> Vec<UnparsedAbrechnungsFile> {
    let mut result = vec![];
    let path = app_root().join(std::path::Path::new(&config.location));
    eprintln!("Lade Abrechnungen aus: {:?}", path);

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
