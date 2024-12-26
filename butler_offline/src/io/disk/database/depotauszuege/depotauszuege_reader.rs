use crate::io::disk::database::depotauszuege::depotauszug_reader::read_depotauszug;
use crate::io::disk::diskrepresentation::file::SortedFile;
use crate::model::database::depotauszug::Depotauszug;

pub fn read_depotauszuege(sorted_file: &SortedFile) -> Vec<Depotauszug> {
    sorted_file
        .depotauszuege
        .iter()
        .map(|l| read_depotauszug(l.into()))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::diskrepresentation::line::builder::line;
    use crate::model::database::depotauszug::builder::{
        demo_depotauszug_aus_str, DEMO_DEPOTAUSZUG_STR,
    };

    #[test]
    fn test_read_depotwerte() {
        let sorted_file = SortedFile {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparbuchungen: vec![],
            sparkontos: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftrag: vec![],
            depotauszuege: vec![line(DEMO_DEPOTAUSZUG_STR)],
        };

        let depotauszuege = read_depotauszuege(&sorted_file);

        assert_eq!(depotauszuege.len(), 1);

        assert_eq!(depotauszuege[0], demo_depotauszug_aus_str());
    }
}
