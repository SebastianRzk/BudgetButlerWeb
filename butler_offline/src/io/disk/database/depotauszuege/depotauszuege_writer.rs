use crate::io::disk::database::depotauszuege::depotauszug_writer::write_depotauszug;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::state::persistent_application_state::Database;

pub fn write_depotauszuege(database: &Database) -> Vec<Line> {
    database
        .depotauszuege
        .depotauszuege
        .iter()
        .map(|l| write_depotauszug(&l.value))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::depotauszug::builder::{
        demo_depotauszug_aus_str, DEMO_DEPOTAUSZUG_STR,
    };
    use crate::model::state::persistent_application_state::builder::{
        demo_database_version, depotauszuege, leere_dauerauftraege, leere_depotwerte,
        leere_einzelbuchungen, leere_gemeinsame_buchungen, leere_order, leere_order_dauerauftraege,
        leere_sparbuchungen, leere_sparkontos,
    };

    #[test]
    fn test_write_depotauszuege() {
        let depotauszug = demo_depotauszug_aus_str();
        let database = Database {
            einzelbuchungen: leere_einzelbuchungen(),
            db_version: demo_database_version(),
            dauerauftraege: leere_dauerauftraege(),
            gemeinsame_buchungen: leere_gemeinsame_buchungen(),
            sparkontos: leere_sparkontos(),
            sparbuchungen: leere_sparbuchungen(),
            depotwerte: leere_depotwerte(),
            order: leere_order(),
            order_dauerauftraege: leere_order_dauerauftraege(),
            depotauszuege: depotauszuege(depotauszug),
        };

        let lines = write_depotauszuege(&database);

        assert_eq!(lines.len(), 1);
        assert_eq!(lines[0].line, DEMO_DEPOTAUSZUG_STR);
    }
}
