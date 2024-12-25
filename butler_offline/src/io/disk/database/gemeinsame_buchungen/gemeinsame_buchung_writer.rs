use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::primitive::betrag::write_betrag;
use crate::io::disk::primitive::datum::write_datum;
use crate::io::disk::primitive::line::create_line;
use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;

pub fn write_gemeinsame_buchung(gemeinsame: &GemeinsameBuchung) -> Line {
    create_line(vec![
        write_datum(&gemeinsame.datum),
        Element::create_escaped(gemeinsame.kategorie.kategorie.clone()),
        Element::create_escaped(gemeinsame.name.get_name().clone()),
        write_betrag(&gemeinsame.betrag),
        Element::create_escaped(gemeinsame.person.person.clone()),
    ])
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::person::builder::person;

    #[test]
    fn test_write_gemeinsame_buchung() {
        let gemeinsame_buchung = GemeinsameBuchung {
            datum: Datum::new(1, 1, 2024),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: betrag(Vorzeichen::Negativ, 123, 12),
            person: person("Test_User"),
        };

        let line = write_gemeinsame_buchung(&gemeinsame_buchung);

        assert_eq!(
            line.line,
            "2024-01-01,NeueKategorie,Normal,-123.12,Test_User"
        );
    }
}
