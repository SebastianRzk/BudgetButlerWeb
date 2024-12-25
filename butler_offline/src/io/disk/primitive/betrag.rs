use crate::io::disk::primitive::segment_reader::Element;
use crate::model::primitives::betrag::Betrag;

pub fn read_betrag(element: Element) -> Betrag {
    Betrag::from_iso_string(&element.element)
}

pub fn write_betrag(betrag: &Betrag) -> Element {
    Element {
        element: betrag.to_iso_string(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};

    #[test]
    fn test_read_negativen_betrag() {
        let ergebnis = read_betrag(element("-123.12"));
        assert_eq!(ergebnis, betrag(Vorzeichen::Negativ, 123, 12));
    }

    #[test]
    fn test_read_positiven_betrag() {
        let ergebnis = read_betrag(element("123.12"));
        assert_eq!(ergebnis, betrag(Vorzeichen::Positiv, 123, 12));
    }

    #[test]
    fn test_write_betrag() {
        let betrag = betrag(Vorzeichen::Negativ, 123, 12);
        let ergebnis = write_betrag(&betrag);
        assert_eq!(ergebnis.element, "-123.12");
    }
}
