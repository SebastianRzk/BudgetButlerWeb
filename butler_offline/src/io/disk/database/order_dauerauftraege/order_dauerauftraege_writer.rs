use crate::io::disk::database::order_dauerauftraege::order_dauerauftrag_writer::write_order_dauerauftrag;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::state::persistent_application_state::Database;

pub fn write_order_dauerauftraege(database: &Database) -> Vec<Line> {
    database
        .order_dauerauftraege
        .order_dauerauftraege
        .iter()
        .map(|l| write_order_dauerauftrag(&l.value))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::order_dauerauftrag::builder::{
        demo_order_dauerauftrag, DEMO_ORDER_DAUERAUFTRAG_AS_DB_STR,
    };
    use crate::model::state::persistent_application_state::builder::generate_database_with_order_dauerauftraege;

    #[test]
    fn test_write_orders() {
        let database = generate_database_with_order_dauerauftraege(vec![demo_order_dauerauftrag()]);

        let lines = write_order_dauerauftraege(&database);

        assert_eq!(lines.len(), 1);
        assert_eq!(lines[0].line, DEMO_ORDER_DAUERAUFTRAG_AS_DB_STR);
    }
}
