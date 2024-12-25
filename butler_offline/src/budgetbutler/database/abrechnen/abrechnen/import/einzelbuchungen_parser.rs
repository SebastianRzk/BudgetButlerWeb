use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::primitive::betrag::read_betrag;
use crate::io::disk::primitive::datum::read_datum;
use crate::io::disk::primitive::segment_reader::{read_next_element, Element};
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;

fn read_einzelbuchung(line: Element) -> Einzelbuchung {
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
pub fn read_einzelbuchungen(lines: Vec<Line>) -> Vec<Einzelbuchung> {
    lines
        .into_iter()
        .map(|line| (&line).into())
        .map(read_einzelbuchung)
        .collect()
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::abrechnen::import::einzelbuchungen_parser::read_einzelbuchungen;
    use crate::io::disk::diskrepresentation::line::builder::line;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::builder::datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;

    #[test]
    fn test_read_einzelbuchungen() {
        let lines = vec![
            line("2024-01-01,NeueKategorie,Normal,-123.12"),
            line("2024-01-02,NeueKategorie2,Normal2,-122.12"),
        ];
        let einzelbuchungen = read_einzelbuchungen(lines);

        assert_eq!(einzelbuchungen.len(), 2);
        assert_eq!(einzelbuchungen.get(0).unwrap().datum, datum("2024-01-01"));
        assert_eq!(
            einzelbuchungen.get(0).unwrap().betrag,
            betrag(Vorzeichen::Negativ, 123, 12)
        );
        assert_eq!(
            einzelbuchungen.get(0).unwrap().kategorie,
            kategorie("NeueKategorie")
        );
        assert_eq!(einzelbuchungen.get(0).unwrap().name, name("Normal"));

        assert_eq!(einzelbuchungen.get(1).unwrap().datum, datum("2024-01-02"));
        assert_eq!(
            einzelbuchungen.get(1).unwrap().betrag,
            betrag(Vorzeichen::Negativ, 122, 12)
        );
        assert_eq!(
            einzelbuchungen.get(1).unwrap().kategorie,
            kategorie("NeueKategorie2")
        );
        assert_eq!(einzelbuchungen.get(1).unwrap().name, name("Normal2"));
    }
}
