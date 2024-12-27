use crate::io::disk::database::einzelbuchungen::einzelbuchung_writer::write_einzelbuchung;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::state::persistent_application_state::Database;

pub fn write_einzelbuchungen(database: &Database) -> Vec<Line> {
    database
        .einzelbuchungen
        .einzelbuchungen
        .iter()
        .filter(|e| !e.dynamisch)
        .map(|e| &e.value)
        .map(|e| write_einzelbuchung(e))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::einzelbuchung::builder::demo_einzelbuchung;
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::indiziert::builder::dynamisch_indiziert;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_application_state::builder::{
        demo_database_version, generate_database_with_einzelbuchungen, leere_dauerauftraege,
        leere_depotauszuege, leere_depotwerte, leere_gemeinsame_buchungen, leere_order,
        leere_order_dauerauftraege, leere_sparbuchungen, leere_sparkontos,
    };
    use crate::model::state::persistent_state::einzelbuchungen::Einzelbuchungen;

    #[test]
    fn test_write_einzelbuchung() {
        let einzelbuchung = Einzelbuchung {
            datum: Datum::new(1, 1, 2024),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: betrag(Vorzeichen::Negativ, 123, 12),
        };
        let database = generate_database_with_einzelbuchungen(vec![einzelbuchung]);

        let lines = write_einzelbuchungen(&database);

        assert_eq!(lines.len(), 1);
        assert_eq!(lines[0].line, "2024-01-01,NeueKategorie,Normal,-123.12");
    }

    #[test]
    fn test_write_einzelbuchung_should_filter_dynamic() {
        let database = Database {
            einzelbuchungen: Einzelbuchungen {
                einzelbuchungen: vec![dynamisch_indiziert(demo_einzelbuchung())],
            },
            db_version: demo_database_version(),
            dauerauftraege: leere_dauerauftraege(),
            gemeinsame_buchungen: leere_gemeinsame_buchungen(),
            sparkontos: leere_sparkontos(),
            sparbuchungen: leere_sparbuchungen(),
            depotwerte: leere_depotwerte(),
            order: leere_order(),
            order_dauerauftraege: leere_order_dauerauftraege(),
            depotauszuege: leere_depotauszuege(),
        };

        let lines = write_einzelbuchungen(&database);

        assert_eq!(lines.len(), 0);
    }
}
