use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::order::OrderTyp;

const KAUF_STR: &str = "Kauf";
const VERKAUF_STR: &str = "Verkauf";
const STEUER_STR: &str = "Steuer";
const DIVIDENDE_STR: &str = "Dividende";
const SONSTIGE_KOSTEN_STR: &str = "Sonstige Kosten";

pub fn read_ordertyp(element: Element) -> OrderTyp {
    match element.element.as_str() {
        KAUF_STR => OrderTyp::Kauf,
        VERKAUF_STR => OrderTyp::Verkauf,
        STEUER_STR => OrderTyp::Steuer,
        DIVIDENDE_STR => OrderTyp::Dividende,
        SONSTIGE_KOSTEN_STR => OrderTyp::SonstigeKosten,
        _ => panic!("Unknown ordertyp {}", element.element),
    }
}

pub fn write_ordertyp(order_typ: OrderTyp) -> Element {
    Element {
        element: match order_typ {
            OrderTyp::Kauf => KAUF_STR.to_string(),
            OrderTyp::Verkauf => VERKAUF_STR.to_string(),
            OrderTyp::Steuer => STEUER_STR.to_string(),
            OrderTyp::Dividende => DIVIDENDE_STR.to_string(),
            OrderTyp::SonstigeKosten => SONSTIGE_KOSTEN_STR.to_string(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;

    #[test]
    fn test_read_depotwerttyp() {
        let etf = element("Kauf");
        assert_eq!(read_ordertyp(etf), OrderTyp::Kauf);

        let fond = element("Verkauf");
        assert_eq!(read_ordertyp(fond), OrderTyp::Verkauf);

        let einzelaktie = element("Steuer");
        assert_eq!(read_ordertyp(einzelaktie), OrderTyp::Steuer);

        let crypto = element("Dividende");
        assert_eq!(read_ordertyp(crypto), OrderTyp::Dividende);

        let robot = element("Sonstige Kosten");
        assert_eq!(read_ordertyp(robot), OrderTyp::SonstigeKosten);
    }

    #[test]
    fn test_write_depotwerttyp() {
        let etf = write_ordertyp(OrderTyp::Kauf);
        assert_eq!(etf.element, "Kauf");

        let fond = write_ordertyp(OrderTyp::Verkauf);
        assert_eq!(fond.element, "Verkauf");

        let einzelaktie = write_ordertyp(OrderTyp::Steuer);
        assert_eq!(einzelaktie.element, "Steuer");

        let crypto = write_ordertyp(OrderTyp::Dividende);
        assert_eq!(crypto.element, "Dividende");

        let robot = write_ordertyp(OrderTyp::SonstigeKosten);
        assert_eq!(robot.element, "Sonstige Kosten");
    }
}
