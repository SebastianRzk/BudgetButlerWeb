use crate::io::disk::diskrepresentation::line::Line;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::person::Person;
use crate::model::state::config::AbrechnungsConfiguration;
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use std::io::Write;
use std::path::Path;

pub fn speichere_abrechnung(
    user_application_directory: &UserApplicationDirectory,
    abrechnung: Vec<Line>,
    person: Person,
    abrechnungs_configuration: AbrechnungsConfiguration,
    today: Datum,
    now: String,
) {
    let file_name = format!(
        "Abrechnung_{}_{}_{}.txt",
        today.to_iso_string(),
        now,
        person.person
    );
    let file_path = user_application_directory
        .path
        .join(Path::new(&abrechnungs_configuration.location))
        .join(file_name);

    let mut file = std::fs::File::create(file_path).unwrap();
    for line in abrechnung {
        file.write_all(line.line.as_bytes()).unwrap();
        file.write_all("\n".as_bytes()).unwrap();
    }
}
