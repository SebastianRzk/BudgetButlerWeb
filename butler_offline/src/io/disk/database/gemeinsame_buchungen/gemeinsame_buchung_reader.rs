use crate::io::disk::primitive::betrag::read_betrag;
use crate::io::disk::primitive::datum::read_datum;
use crate::io::disk::primitive::segment_reader::{read_next_element, Element};
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::person::Person;

pub fn read_gemeinsame_buchung(line: Element) -> GemeinsameBuchung {
    let datum_segment = read_next_element(line);
    let datum = read_datum(datum_segment.element);

    let kategorie_segment = read_next_element(datum_segment.rest);
    let name_segment = read_next_element(kategorie_segment.rest);
    let betrag_segment = read_next_element(name_segment.rest);
    let betrag = read_betrag(betrag_segment.element);
    let person = read_next_element(betrag_segment.rest).element.element;

    GemeinsameBuchung {
        datum,
        name: Name::new(name_segment.element.element),
        kategorie: Kategorie::new(kategorie_segment.element.element),
        betrag,
        person: Person::new(person),
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
    use crate::model::primitives::person::builder::person;

    #[test]
    fn test_read_gemeinsame_buchung() {
        let line = element("2024-11-01,NeueKategorie,Name,-234.12,Test_User");
        let gemeinsame_buchung = read_gemeinsame_buchung(line);
        assert_eq!(gemeinsame_buchung.datum, Datum::new(1, 11, 2024));
        assert_eq!(gemeinsame_buchung.name, name("Name"));
        assert_eq!(gemeinsame_buchung.kategorie, kategorie("NeueKategorie"));
        assert_eq!(
            gemeinsame_buchung.betrag,
            betrag(Vorzeichen::Negativ, 234, 12)
        );
        assert_eq!(gemeinsame_buchung.person, person("Test_User"));
    }
}
