use crate::io::disk::database::sparkontos::sparkonto_reader::read_sparkonto;
use crate::io::disk::diskrepresentation::file::SortedFile;
use crate::model::database::sparkonto::Sparkonto;

pub fn read_sparkontos(sorted_file: &SortedFile) -> Vec<Sparkonto> {
    sorted_file
        .sparkontos
        .iter()
        .map(|l| read_sparkonto(l.into()))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::diskrepresentation::line::builder::line;
    use crate::model::database::sparkonto::Kontotyp;
    use crate::model::primitives::name::name;

    #[test]
    fn test_read_sparkontos() {
        let sorted_file = SortedFile {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparbuchungen: vec![],
            sparkontos: vec![
                line("MeinSparkonto,Sparkonto"),
                line("MeineGenossenschaftsanteile,Genossenschafts-Anteile"),
            ],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftrag: vec![],
            depotauszuege: vec![],
        };

        let sparkontos = read_sparkontos(&sorted_file);
        let sparkonto_eins = &sparkontos[0];

        assert_eq!(sparkonto_eins.name, name("MeinSparkonto"));
        assert_eq!(sparkonto_eins.kontotyp, Kontotyp::Sparkonto);

        let sparkonto_zwei = &sparkontos[1];
        assert_eq!(sparkonto_zwei.name, name("MeineGenossenschaftsanteile"));
        assert_eq!(sparkonto_zwei.kontotyp, Kontotyp::GenossenschaftsAnteile);
    }
}
