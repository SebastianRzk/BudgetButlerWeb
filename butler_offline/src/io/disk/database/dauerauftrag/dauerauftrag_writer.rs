use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::primitive::betrag::write_betrag;
use crate::io::disk::primitive::datum::write_datum;
use crate::io::disk::primitive::line::create_line;
use crate::io::disk::primitive::rhythmus::write_rhythmus;
use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::dauerauftrag::Dauerauftrag;

pub fn write_dauerauftrag(dauerauftrag: &Dauerauftrag) -> Line {
    create_line(vec![
        write_datum(&dauerauftrag.start_datum),
        write_datum(&dauerauftrag.ende_datum),
        Element::create_escaped(dauerauftrag.kategorie.kategorie.clone()),
        Element::create_escaped(dauerauftrag.name.get_name().clone()),
        write_rhythmus(dauerauftrag.rhythmus),
        write_betrag(&dauerauftrag.betrag),
    ])
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::rhythmus::Rhythmus;

    #[test]
    fn test_write_dauerauftrag() {
        let dauerauftrag = Dauerauftrag {
            start_datum: Datum::new(1, 1, 2024),
            ende_datum: Datum::new(1, 1, 2025),
            name: name("Miete"),
            kategorie: kategorie("NeueKategorie"),
            rhythmus: Rhythmus::Monatlich,
            betrag: betrag(Vorzeichen::Negativ, 123, 12),
        };

        let line = write_dauerauftrag(&dauerauftrag);

        assert_eq!(
            line.line,
            "2024-01-01,2025-01-01,NeueKategorie,Miete,monatlich,-123.12"
        );
    }
}
