use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::primitive::line::create_line;
use crate::io::disk::primitive::order_typ::write_ordertyp;
use crate::io::disk::primitive::rhythmus::write_rhythmus;
use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::order_dauerauftrag::OrderDauerauftrag;

pub fn write_order_dauerauftrag(order_dauerauftrag: &OrderDauerauftrag) -> Line {
    create_line(vec![
        Element::new(order_dauerauftrag.start_datum.to_iso_string()),
        Element::new(order_dauerauftrag.ende_datum.to_iso_string()),
        write_rhythmus(order_dauerauftrag.rhythmus.clone()),
        Element::new(order_dauerauftrag.name.to_string()),
        Element::new(order_dauerauftrag.konto.konto_name.get_name().clone()),
        Element::new(order_dauerauftrag.depotwert.isin.isin.clone()),
        Element::new(order_dauerauftrag.wert.get_realer_wert().to_iso_string()),
        write_ordertyp(order_dauerauftrag.wert.get_typ()),
    ])
}

#[cfg(test)]
mod tests {
    use crate::io::disk::database::order_dauerauftraege::order_dauerauftrag_writer::write_order_dauerauftrag;
    use crate::model::database::order_dauerauftrag::builder::{
        demo_order_dauerauftrag, DEMO_ORDER_DAUERAUFTRAG_AS_DB_STR,
    };

    #[test]
    fn test_write_order_dauerauftrag() {
        let line = write_order_dauerauftrag(&demo_order_dauerauftrag());

        assert_eq!(line.line, DEMO_ORDER_DAUERAUFTRAG_AS_DB_STR);
    }
}
