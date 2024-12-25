use crate::io::disk::database::einzelbuchungen::einzelbuchung_reader::read_einzelbuchung;
use crate::io::disk::diskrepresentation::file::SortedFile;
use crate::model::database::einzelbuchung::Einzelbuchung;

pub fn read_einzelbuchungen(sorted_file: &SortedFile) -> Vec<Einzelbuchung> {
    sorted_file
        .einzelbuchungen
        .iter()
        .map(|l| read_einzelbuchung(l.into()))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::diskrepresentation::line::builder::line;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;

    #[test]
    fn test_read_einzelbuchungen() {
        let sorted_file = SortedFile {
            einzelbuchungen: vec![
                line("2024-01-01,NeueKategorie,Normal,-123.12"),
                line("2024-01-02,NeueKategorie2,Normal2,-123.13"),
            ],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparbuchungen: vec![],
            sparkontos: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftrag: vec![],
            depotauszuege: vec![],
        };

        let einzelbuchungen = read_einzelbuchungen(&sorted_file);
        assert_eq!(einzelbuchungen[0].datum, Datum::new(1, 1, 2024));
        assert_eq!(einzelbuchungen[0].name, name("Normal"));
        assert_eq!(einzelbuchungen[0].kategorie, kategorie("NeueKategorie"));
        assert_eq!(
            einzelbuchungen[0].betrag,
            betrag(Vorzeichen::Negativ, 123, 12)
        );
        assert_eq!(einzelbuchungen[1].datum, Datum::new(2, 1, 2024));
        assert_eq!(einzelbuchungen[1].name, name("Normal2"));
        assert_eq!(einzelbuchungen[1].kategorie, kategorie("NeueKategorie2"));
        assert_eq!(
            einzelbuchungen[1].betrag,
            betrag(Vorzeichen::Negativ, 123, 13)
        );
    }
}
