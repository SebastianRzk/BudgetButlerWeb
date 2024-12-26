use crate::io::disk::database::sparbuchungen::sparbuchung_reader::read_sparbuchung;
use crate::io::disk::diskrepresentation::file::SortedFile;
use crate::model::database::sparbuchung::Sparbuchung;

pub fn read_sparbuchungen(sorted_file: &SortedFile) -> Vec<Sparbuchung> {
    sorted_file
        .sparbuchungen
        .iter()
        .map(|l| read_sparbuchung(l.into()))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::diskrepresentation::line::builder::line;
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::database::sparbuchung::SparbuchungTyp;
    use crate::model::primitives::betrag::builder::u_betrag;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::name;

    #[test]
    fn test_read_dauerauftraege() {
        let sorted_file = SortedFile {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparbuchungen: vec![
                line("2024-01-01,DerName,123.12,Zinsen,DasKonto"),
                line("2024-01-02,DerName2,123.13,Ausschüttung,DasKonto2"),
            ],
            sparkontos: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftrag: vec![],
            depotauszuege: vec![],
        };

        let sparbuchungen = read_sparbuchungen(&sorted_file);
        let sparbuchung_eins = &sparbuchungen[0];
        assert_eq!(sparbuchung_eins.datum, Datum::new(1, 1, 2024));
        assert_eq!(sparbuchung_eins.name, name("DerName"));
        assert_eq!(sparbuchung_eins.wert, u_betrag(123, 12));
        assert_eq!(sparbuchung_eins.typ, SparbuchungTyp::Zinsen);
        assert_eq!(sparbuchung_eins.konto, konto_referenz("DasKonto"));

        let sparbuchung_zwei = &sparbuchungen[1];
        assert_eq!(sparbuchung_zwei.datum, Datum::new(2, 1, 2024));
        assert_eq!(sparbuchung_zwei.name, name("DerName2"));
        assert_eq!(sparbuchung_zwei.wert, u_betrag(123, 13));
        assert_eq!(sparbuchung_zwei.typ, SparbuchungTyp::Ausschuettung);
        assert_eq!(sparbuchung_zwei.konto, konto_referenz("DasKonto2"));
    }
}
