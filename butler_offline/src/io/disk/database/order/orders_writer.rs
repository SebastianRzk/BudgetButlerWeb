use crate::io::disk::database::order::order_writer::write_order;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::state::persistent_application_state::Database;

pub fn write_orders(database: &Database) -> Vec<Line> {
    database
        .order
        .orders
        .iter()
        .filter(|l| !l.dynamisch)
        .map(|l| write_order(&l.value))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::order::builder::{any_order, demo_order, DEMO_ORDER_AS_DB_STR};
    use crate::model::indiziert::builder::dynamisch_indiziert;
    use crate::model::state::persistent_application_state::builder::{
        demo_database_version, generate_database_with_orders, leere_dauerauftraege,
        leere_depotauszuege, leere_depotwerte, leere_einzelbuchungen, leere_gemeinsame_buchungen,
        leere_order_dauerauftraege, leere_sparbuchungen, leere_sparkontos,
    };
    use crate::model::state::persistent_state::order::Orders;

    #[test]
    fn test_write_orders() {
        let database = generate_database_with_orders(vec![demo_order()]);

        let lines = write_orders(&database);

        assert_eq!(lines.len(), 1);
        assert_eq!(lines[0].line, DEMO_ORDER_AS_DB_STR);
    }

    #[test]
    fn test_should_filter_dynamic_order() {
        let database = Database {
            order: Orders {
                orders: vec![dynamisch_indiziert(any_order())],
            },
            db_version: demo_database_version(),
            dauerauftraege: leere_dauerauftraege(),
            gemeinsame_buchungen: leere_gemeinsame_buchungen(),
            sparkontos: leere_sparkontos(),
            sparbuchungen: leere_sparbuchungen(),
            depotwerte: leere_depotwerte(),
            order_dauerauftraege: leere_order_dauerauftraege(),
            einzelbuchungen: leere_einzelbuchungen(),
            depotauszuege: leere_depotauszuege(),
        };

        let lines = write_orders(&database);

        assert_eq!(lines.len(), 0);
    }
}
