use crate::io::disk::database::gemeinsame_buchungen::gemeinsame_buchung_writer::write_gemeinsame_buchung;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::state::persistent_application_state::Database;

pub fn write_gemeinsame_buchungen(database: &Database) -> Vec<Line> {
    database
        .gemeinsame_buchungen
        .gemeinsame_buchungen
        .iter()
        .map(|e| &e.value)
        .map(|e| write_gemeinsame_buchung(e))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::person::builder::person;
    use crate::model::state::persistent_application_state::builder::generate_database_with_gemeinsamen_buchungen;

    #[test]
    fn test_write_gemeinsame_buchungen() {
        let gemeinsame_buchung = GemeinsameBuchung {
            datum: Datum::new(1, 1, 2024),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: betrag(Vorzeichen::Negativ, 123, 12),
            person: person("Test_User"),
        };
        let database = generate_database_with_gemeinsamen_buchungen(vec![gemeinsame_buchung]);

        let lines = write_gemeinsame_buchungen(&database);

        assert_eq!(lines.len(), 1);
        assert_eq!(
            lines[0].line,
            "2024-01-01,NeueKategorie,Normal,-123.12,Test_User"
        );
    }
}
