use crate::io::disk::primitive::segment_reader::Element;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;

pub fn read_betrag_ohne_vorzeichen(element: Element) -> BetragOhneVorzeichen {
    BetragOhneVorzeichen::from_iso_string(&element.element)
}

pub fn write_betrag_ohne_vorzeichen(betrag: &BetragOhneVorzeichen) -> Element {
    Element {
        element: betrag.to_iso_string(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;

    #[test]
    fn test_read_betrag() {
        let ergebnis = read_betrag_ohne_vorzeichen(element("123.12"));
        assert_eq!(ergebnis, BetragOhneVorzeichen::new(123, 12));
    }

    #[test]
    fn test_write_betrag() {
        let betrag = BetragOhneVorzeichen::new(123, 12);
        let ergebnis = write_betrag_ohne_vorzeichen(&betrag);
        assert_eq!(ergebnis.element, "123.12");
    }
}
