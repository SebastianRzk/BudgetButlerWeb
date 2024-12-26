use crate::io::disk::database::depotwerte::depotwert_reader::read_depotwert;
use crate::io::disk::diskrepresentation::file::SortedFile;
use crate::model::database::depotwert::Depotwert;

pub fn read_depotwerte(sorted_file: &SortedFile) -> Vec<Depotwert> {
    sorted_file
        .depotwerte
        .iter()
        .map(|l| read_depotwert(l.into()))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::diskrepresentation::line::builder::line;
    use crate::model::database::depotwert::DepotwertTyp;
    use crate::model::primitives::isin::builder::isin;
    use crate::model::primitives::name::name;

    #[test]
    fn test_read_depotwerte() {
        let sorted_file = SortedFile {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparbuchungen: vec![],
            sparkontos: vec![],
            depotwerte: vec![
                line("MeinDepotwert,DE000A0D9PT0,ETF"),
                line("MeineGenossenschaftsanteile,DE000A0D9PT1,Robot"),
            ],
            order: vec![],
            order_dauerauftrag: vec![],
            depotauszuege: vec![],
        };

        let depotwerte = read_depotwerte(&sorted_file);

        assert_eq!(depotwerte.len(), 2);

        assert_eq!(depotwerte[0].name, name("MeinDepotwert"));
        assert_eq!(depotwerte[0].isin, isin("DE000A0D9PT0"));
        assert_eq!(depotwerte[0].typ, DepotwertTyp::ETF);

        assert_eq!(depotwerte[1].name, name("MeineGenossenschaftsanteile"));
        assert_eq!(depotwerte[1].isin, isin("DE000A0D9PT1"));
        assert_eq!(depotwerte[1].typ, DepotwertTyp::Robot);
    }
}
