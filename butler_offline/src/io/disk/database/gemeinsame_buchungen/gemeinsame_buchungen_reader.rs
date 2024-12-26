use crate::io::disk::database::gemeinsame_buchungen::gemeinsame_buchung_reader::read_gemeinsame_buchung;
use crate::io::disk::diskrepresentation::file::SortedFile;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;

pub fn read_gemeinsame_buchungen(sorted_file: &SortedFile) -> Vec<GemeinsameBuchung> {
    sorted_file
        .gemeinsame_buchungen
        .iter()
        .map(|l| read_gemeinsame_buchung(l.into()))
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
    use crate::model::primitives::person::builder::person;

    #[test]
    fn test_read_gemeinsame_buchungen() {
        let sorted_file = SortedFile {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![
                line("2024-01-01,NeueKategorie,Normal,-123.12,Test_User,True"),
                line("2024-01-02,NeueKategorie2,Normal2,-123.13,kein_Partnername_gesetzt"),
            ],
            sparbuchungen: vec![],
            sparkontos: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftrag: vec![],
            depotauszuege: vec![],
        };

        let gemeinsame_buchungen = read_gemeinsame_buchungen(&sorted_file);
        assert_eq!(gemeinsame_buchungen[0].datum, Datum::new(1, 1, 2024));
        assert_eq!(gemeinsame_buchungen[0].name, name("Normal"));
        assert_eq!(
            gemeinsame_buchungen[0].kategorie,
            kategorie("NeueKategorie")
        );
        assert_eq!(
            gemeinsame_buchungen[0].betrag,
            betrag(Vorzeichen::Negativ, 123, 12)
        );
        assert_eq!(gemeinsame_buchungen[0].person, person("Test_User"));

        assert_eq!(gemeinsame_buchungen[1].datum, Datum::new(2, 1, 2024));
        assert_eq!(gemeinsame_buchungen[1].name, name("Normal2"));
        assert_eq!(
            gemeinsame_buchungen[1].kategorie,
            kategorie("NeueKategorie2")
        );
        assert_eq!(
            gemeinsame_buchungen[1].betrag,
            betrag(Vorzeichen::Negativ, 123, 13)
        );
        assert_eq!(
            gemeinsame_buchungen[1].person,
            person("kein_Partnername_gesetzt")
        );
    }
}
