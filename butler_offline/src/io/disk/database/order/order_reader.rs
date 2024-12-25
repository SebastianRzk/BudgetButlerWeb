use crate::io::disk::primitive::betrag_ohne_vorzeichen::read_betrag_ohne_vorzeichen;
use crate::io::disk::primitive::datum::read_datum;
use crate::io::disk::primitive::order_typ::read_ordertyp;
use crate::io::disk::primitive::segment_reader::{read_next_element, Element};
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::order::Order;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::name::Name;
use crate::model::primitives::order_betrag::OrderBetrag;

pub fn read_order(line: Element) -> Order {
    let datum_segment = read_next_element(line);
    let datum = read_datum(datum_segment.element);

    let name_segment = read_next_element(datum_segment.rest);

    let konto_segment = read_next_element(name_segment.rest);

    let depotwert_segment = read_next_element(konto_segment.rest);

    let wert_segment = read_next_element(depotwert_segment.rest);
    let wert = read_betrag_ohne_vorzeichen(wert_segment.element);
    let typ = read_ordertyp(wert_segment.rest);

    Order {
        datum,
        name: Name::new(name_segment.element.element),
        konto: KontoReferenz::new(Name::new(konto_segment.element.element)),
        depotwert: DepotwertReferenz::new(ISIN::new(depotwert_segment.element.element)),
        wert: OrderBetrag::new(wert, typ),
    }
}

#[cfg(test)]
mod tests {
    use crate::io::disk::database::order::order_reader::read_order;
    use crate::io::disk::primitive::segment_reader::builder::element;
    use crate::model::database::order::builder::{demo_order, DEMO_ORDER_AS_DB_STR};

    #[test]
    fn test_read_order() {
        let line = element(DEMO_ORDER_AS_DB_STR);
        let order = read_order(line);

        assert_eq!(order, demo_order());
    }
}
