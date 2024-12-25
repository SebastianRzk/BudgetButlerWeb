use crate::io::disk::database::dauerauftrag::dauerauftrag_reader::read_dauerauftrag;
use crate::io::disk::diskrepresentation::file::SortedFile;
use crate::model::database::dauerauftrag::Dauerauftrag;

pub fn read_dauerauftraege(sorted_file: &SortedFile) -> Vec<Dauerauftrag> {
    sorted_file
        .dauerauftraege
        .iter()
        .map(|l| read_dauerauftrag(l.into()))
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
    use crate::model::primitives::rhythmus::Rhythmus;

    #[test]
    fn test_read_dauerauftraege() {
        let sorted_file = SortedFile {
            einzelbuchungen: vec![],
            dauerauftraege: vec![
                line("2024-01-01,2025-01-01,NeueKategorie,Miete,monatlich,-123.12"),
                line("2024-01-02,2025-01-02,NeueKategorie2,Miete2,monatlich,-123.13"),
            ],
            gemeinsame_buchungen: vec![],
            sparbuchungen: vec![],
            sparkontos: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftrag: vec![],
            depotauszuege: vec![],
        };

        let dauerauftraege = read_dauerauftraege(&sorted_file);
        let dauerauftrag_eins = &dauerauftraege[0];
        assert_eq!(dauerauftrag_eins.start_datum, Datum::new(1, 1, 2024));
        assert_eq!(dauerauftrag_eins.ende_datum, Datum::new(1, 1, 2025));
        assert_eq!(dauerauftrag_eins.name, name("Miete"));
        assert_eq!(dauerauftrag_eins.kategorie, kategorie("NeueKategorie"));
        assert_eq!(dauerauftrag_eins.rhythmus, Rhythmus::Monatlich);
        assert_eq!(
            dauerauftrag_eins.betrag,
            betrag(Vorzeichen::Negativ, 123, 12)
        );

        let dauerauftrag_zwei = &dauerauftraege[1];
        assert_eq!(dauerauftrag_zwei.start_datum, Datum::new(2, 1, 2024));
        assert_eq!(dauerauftrag_zwei.ende_datum, Datum::new(2, 1, 2025));
        assert_eq!(dauerauftrag_zwei.name, name("Miete2"));
        assert_eq!(dauerauftrag_zwei.kategorie, kategorie("NeueKategorie2"));
        assert_eq!(dauerauftrag_zwei.rhythmus, Rhythmus::Monatlich);
        assert_eq!(
            dauerauftrag_zwei.betrag,
            betrag(Vorzeichen::Negativ, 123, 13)
        );
    }
}
