use crate::io::disk::database::depotwerte::depotwert_writer::write_depotwert;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::state::persistent_application_state::Database;

pub fn write_depotwerte(database: &Database) -> Vec<Line> {
    database
        .depotwerte
        .depotwerte
        .iter()
        .map(|l| write_depotwert(&l.value))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::depotwert::{Depotwert, DepotwertTyp};
    use crate::model::primitives::isin::builder::isin;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_application_state::builder::{
        demo_database_version, depotwerte, leere_dauerauftraege, leere_depotauszuege,
        leere_einzelbuchungen, leere_gemeinsame_buchungen, leere_order, leere_order_dauerauftraege,
        leere_sparbuchungen, leere_sparkontos,
    };

    #[test]
    fn test_write_depotwerte() {
        let depotwert = Depotwert {
            name: name("MeinDepotwert"),
            isin: isin("DE000A0D9PT0"),
            typ: DepotwertTyp::ETF,
        };
        let database = Database {
            einzelbuchungen: leere_einzelbuchungen(),
            db_version: demo_database_version(),
            dauerauftraege: leere_dauerauftraege(),
            gemeinsame_buchungen: leere_gemeinsame_buchungen(),
            sparkontos: leere_sparkontos(),
            sparbuchungen: leere_sparbuchungen(),
            depotwerte: depotwerte(depotwert),
            order: leere_order(),
            order_dauerauftraege: leere_order_dauerauftraege(),
            depotauszuege: leere_depotauszuege(),
        };

        let lines = write_depotwerte(&database);

        assert_eq!(lines.len(), 1);
        assert_eq!(lines[0].line, "MeinDepotwert,DE000A0D9PT0,ETF");
    }
}
