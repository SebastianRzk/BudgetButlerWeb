use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::primitive::betrag::write_betrag;
use crate::io::disk::primitive::datum::write_datum;
use crate::io::disk::primitive::line::create_line;
use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::einzelbuchung::Einzelbuchung;

pub fn write_einzelbuchung(einzelbuchung: &Einzelbuchung) -> Line {
    create_line(vec![
        write_datum(&einzelbuchung.datum),
        Element::create_escaped(einzelbuchung.kategorie.kategorie.clone()),
        Element::create_escaped(einzelbuchung.name.get_name().clone()),
        write_betrag(&einzelbuchung.betrag),
    ])
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;

    #[test]
    fn test_write_einzelbuchung() {
        let einzelbuchung = Einzelbuchung {
            datum: Datum::new(1, 1, 2024),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: betrag(Vorzeichen::Negativ, 123, 12),
        };

        let line = write_einzelbuchung(&einzelbuchung);

        assert_eq!(line.line, "2024-01-01,NeueKategorie,Normal,-123.12");
    }
}
