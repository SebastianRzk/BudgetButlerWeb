use crate::io::disk::primitive::betrag::read_betrag;
use crate::io::disk::primitive::datum::read_datum;
use crate::io::disk::primitive::rhythmus::read_rhythmus;
use crate::io::disk::primitive::segment_reader::{read_next_element, Element};
use crate::model::database::dauerauftrag::Dauerauftrag;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;

pub fn read_dauerauftrag(line: Element) -> Dauerauftrag {
    let start_datum_segment = read_next_element(line);
    let start_datum = read_datum(start_datum_segment.element);
    let ende_datum_segment = read_next_element(start_datum_segment.rest);
    let ende_datum = read_datum(ende_datum_segment.element);
    let kategorie_segment = read_next_element(ende_datum_segment.rest);
    let name_segment = read_next_element(kategorie_segment.rest);
    let rhythmus_segment = read_next_element(name_segment.rest);
    let betrag_segment = read_next_element(rhythmus_segment.rest);
    let betrag = read_betrag(betrag_segment.element);

    Dauerauftrag {
        start_datum,
        ende_datum,
        rhythmus: read_rhythmus(rhythmus_segment.element),
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
    use crate::model::primitives::rhythmus::Rhythmus;

    #[test]
    fn test_read_dauerauftrag() {
        let line = element("2024-01-01,2025-01-01,NeueKategorie,Miete,monatlich,-123.12");
        let dauerauftrag = read_dauerauftrag(line);
        assert_eq!(dauerauftrag.start_datum, Datum::new(1, 1, 2024));
        assert_eq!(dauerauftrag.ende_datum, Datum::new(1, 1, 2025));
        assert_eq!(dauerauftrag.name, name("Miete"));
        assert_eq!(dauerauftrag.kategorie, kategorie("NeueKategorie"));
        assert_eq!(dauerauftrag.rhythmus, Rhythmus::Monatlich);
        assert_eq!(dauerauftrag.betrag, betrag(Vorzeichen::Negativ, 123, 12));
    }
}
