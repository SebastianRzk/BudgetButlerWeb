use crate::budgetbutler::database::reader::reader::create_database;
use crate::io::disk::dauerauftrag::dauerauftraege_reader::read_dauerauftraege;
use crate::io::disk::diskrepresentation::file::File;
use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::diskrepresentation::sorter::sort_file;
use crate::io::disk::einzelbuchungen::einzelbuchungen_reader::read_einzelbuchungen;
use crate::io::disk::gemeinsame_buchungen::gemeinsame_buchungen_reader::read_gemeinsame_buchungen;
use crate::io::time::today;
use crate::model::state::config::DatabaseConfiguration;
use crate::model::state::persistent_application_state::{DataOnDisk, Database, DatabaseVersion};
use std::fs;
use std::path::{Path, PathBuf};

fn read_file(path: PathBuf) -> File {
    println!("loading file {}", path.to_str().unwrap());
    let file_as_string = fs::read_to_string::<PathBuf>(path).unwrap();
    let lines = file_as_string.lines().map(|l| Line {
        line: l.to_string(),
    }).collect();
    File { lines }
}


fn read_data(file: File) -> DataOnDisk {
    let sorted_file = sort_file(file);
    DataOnDisk {
        einzelbuchungen: read_einzelbuchungen(&sorted_file),
        dauerauftraege: read_dauerauftraege(&sorted_file),
        gemeinsame_buchungen: read_gemeinsame_buchungen(&sorted_file),
    }
}

pub fn read_database(config: &DatabaseConfiguration, current_database_version: DatabaseVersion) -> Database {
    let file = read_file(Path::new(config.location.as_str()).to_path_buf());
    let data = read_data(file);

    create_database(data, today(), current_database_version)
}

#[cfg(test)]
mod tests {
    use crate::io::disk::diskrepresentation::file::File;
    use crate::io::disk::reader::read_data;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;

    #[test]
    fn test_read_data() {
        let file = File::from_str("2024-01-01,NeueKategorie,Normal,-123.12\n2024-01-02,NeueKategorie2,Normal2,-123.13");
        let data = read_data(file);

        let erste_einzelbuchung = &data.einzelbuchungen[0];
        assert_eq!(erste_einzelbuchung.datum, Datum::new(1, 1, 2024));
        assert_eq!(erste_einzelbuchung.name, name("Normal"));
        assert_eq!(erste_einzelbuchung.kategorie, kategorie("NeueKategorie"));
        assert_eq!(erste_einzelbuchung.betrag, Betrag::new(crate::model::primitives::betrag::Vorzeichen::Negativ, 123, 12));

        let zweite_einzelbuchung = &data.einzelbuchungen[1];
        assert_eq!(zweite_einzelbuchung.datum, Datum::new(2, 1, 2024));
        assert_eq!(zweite_einzelbuchung.name, name("Normal2"));
        assert_eq!(zweite_einzelbuchung.kategorie, kategorie("NeueKategorie2"));
        assert_eq!(zweite_einzelbuchung.betrag, Betrag::new(crate::model::primitives::betrag::Vorzeichen::Negativ, 123, 13));
    }
}