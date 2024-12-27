use crate::io::disk::database::sparbuchungen::sparbuchung_writer::write_sparbuchung;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::state::persistent_application_state::Database;

pub fn write_sparbuchungen(database: &Database) -> Vec<Line> {
    database
        .sparbuchungen
        .sparbuchungen
        .iter()
        .filter(|e| !e.dynamisch)
        .map(|l| write_sparbuchung(&l.value))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::database::sparbuchung::{Sparbuchung, SparbuchungTyp};
    use crate::model::indiziert::builder::dynamisch_indiziert;
    use crate::model::primitives::betrag::builder::u_betrag;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_application_state::builder::{
        demo_database_version, generate_database_with_sparbuchungen, leere_dauerauftraege,
        leere_depotauszuege, leere_depotwerte, leere_einzelbuchungen, leere_gemeinsame_buchungen,
        leere_order, leere_order_dauerauftraege, leere_sparkontos,
    };
    use crate::model::state::persistent_state::sparbuchungen::Sparbuchungen;

    #[test]
    fn test_write_sparbuchung() {
        let sparbuchung = Sparbuchung {
            datum: Datum::new(1, 1, 2024),
            name: name("DerName"),
            wert: u_betrag(123, 12),
            typ: SparbuchungTyp::Ausschuettung,
            konto: konto_referenz("DasKonto"),
        };
        let database = generate_database_with_sparbuchungen(vec![sparbuchung]);

        let lines = write_sparbuchungen(&database);

        assert_eq!(lines.len(), 1);
        assert_eq!(
            lines[0].line,
            "2024-01-01,DerName,123.12,Ausschüttung,DasKonto"
        );
    }

    #[test]
    fn test_should_filter_dynamic() {
        let sparbuchung = Sparbuchung {
            datum: Datum::new(1, 1, 2024),
            name: name("DerName"),
            wert: u_betrag(123, 12),
            typ: SparbuchungTyp::Ausschuettung,
            konto: konto_referenz("DasKonto"),
        };
        let database = Database {
            einzelbuchungen: leere_einzelbuchungen(),
            db_version: demo_database_version(),
            dauerauftraege: leere_dauerauftraege(),
            gemeinsame_buchungen: leere_gemeinsame_buchungen(),
            sparkontos: leere_sparkontos(),
            sparbuchungen: Sparbuchungen {
                sparbuchungen: vec![dynamisch_indiziert(sparbuchung)],
            },
            depotwerte: leere_depotwerte(),
            order: leere_order(),
            order_dauerauftraege: leere_order_dauerauftraege(),
            depotauszuege: leere_depotauszuege(),
        };

        let lines = write_sparbuchungen(&database);

        assert_eq!(lines.len(), 0);
    }
}
