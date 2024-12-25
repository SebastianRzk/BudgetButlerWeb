use crate::io::disk::primitive::betrag::read_betrag;
use crate::io::disk::primitive::datum::read_datum;
use crate::io::disk::primitive::segment_reader::{read_next_element, Element};
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;

pub fn read_einzelbuchung(line: Element) -> Einzelbuchung {
    let datum_segment = read_next_element(line);
    let datum = read_datum(datum_segment.element);
    let kategorie_segment = read_next_element(datum_segment.rest);
    let name_segment = read_next_element(kategorie_segment.rest);
    let betrag_segment = read_next_element(name_segment.rest);
    let betrag = read_betrag(betrag_segment.element);

    Einzelbuchung {
        datum,
        name: Name::new(name_segment.element.element),
        kategorie: Kategorie::new(kategorie_segment.element.element),
        betrag,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;

    #[test]
    fn test_read_einzelbuchung() {
        let line = element("2024-01-01,NeueKategorie,Normal,-123.12");
        let einzelbuchung = read_einzelbuchung(line);
        assert_eq!(einzelbuchung.datum, Datum::new(1, 1, 2024));
        assert_eq!(einzelbuchung.name, name("Normal"));
        assert_eq!(einzelbuchung.kategorie, kategorie("NeueKategorie"));
        assert_eq!(einzelbuchung.betrag, betrag(Vorzeichen::Negativ, 123, 12));
    }
}
