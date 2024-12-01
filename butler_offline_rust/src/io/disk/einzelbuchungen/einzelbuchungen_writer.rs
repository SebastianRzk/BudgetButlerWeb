use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::einzelbuchungen::einzelbuchung_writer::write_einzelbuchung;
use crate::model::state::persistent_application_state::Database;

pub fn write_einzelbuchungen(database: &Database) -> Vec<Line> {
    database.einzelbuchungen.einzelbuchungen.iter()
        .filter(|e| !e.dynamisch)
        .map(|e| &e.value)
        .map(|e| write_einzelbuchung(e)).collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::einzelbuchung::builder::any_einzelbuchung;
    use crate::model::einzelbuchung::Einzelbuchung;
    use crate::model::indiziert::Indiziert;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_application_state::builder::{einzelbuchungen, empty_database_version, leere_dauerauftraege, leere_gemeinsame_buchungen};
    use crate::model::state::persistent_application_state::Einzelbuchungen;

    #[test]
    fn test_write_einzelbuchung() {
        let einzelbuchung = Einzelbuchung {
            datum: Datum::new(1, 1, 2024),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: betrag(Vorzeichen::Negativ, 123, 12),
        };
        let database = Database {
            einzelbuchungen: einzelbuchungen(einzelbuchung),
            db_version: empty_database_version(),
            dauerauftraege: leere_dauerauftraege(),
            gemeinsame_buchungen: leere_gemeinsame_buchungen(),
        };

        let lines = write_einzelbuchungen(&database);

        assert_eq!(lines.len(), 1);
        assert_eq!(lines[0].line, "2024-01-01,NeueKategorie,Normal,-123.12");
    }

    #[test]
    fn test_write_einzelbuchung_should_filter_dynamic() {
        let database = Database {
            einzelbuchungen: Einzelbuchungen {
                einzelbuchungen: vec![
                    Indiziert {
                        value: any_einzelbuchung(),
                        index: 0,
                        dynamisch: true
                    }
                ]
            },
            db_version: empty_database_version(),
            dauerauftraege: leere_dauerauftraege(),
            gemeinsame_buchungen: leere_gemeinsame_buchungen(),
        };

        let lines = write_einzelbuchungen(&database);

        assert_eq!(lines.len(), 0);
    }
}