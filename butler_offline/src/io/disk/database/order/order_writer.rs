use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::primitive::line::create_line;
use crate::io::disk::primitive::order_typ::write_ordertyp;
use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::order::Order;

pub fn write_order(order: &Order) -> Line {
    create_line(vec![
        Element::new(order.datum.to_iso_string()),
        Element::new(order.name.to_string()),
        Element::new(order.konto.konto_name.get_name().clone()),
        Element::new(order.depotwert.isin.isin.clone()),
        Element::new(order.wert.get_realer_wert().to_iso_string()),
        write_ordertyp(order.wert.get_typ()),
    ])
}

#[cfg(test)]
mod tests {
    use crate::io::disk::database::order::order_writer::write_order;
    use crate::model::database::order::builder::{demo_order, DEMO_ORDER_AS_DB_STR};

    #[test]
    fn test_write_order() {
        let order = demo_order();

        let line = write_order(&order);

        assert_eq!(line.line, DEMO_ORDER_AS_DB_STR);
    }
}
