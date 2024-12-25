use crate::io::disk::database::order_dauerauftraege::order_dauerauftrag_reader::read_order_dauerauftrag;
use crate::io::disk::diskrepresentation::file::SortedFile;
use crate::model::database::order_dauerauftrag::OrderDauerauftrag;

pub fn read_order_dauerauftraege(sorted_file: &SortedFile) -> Vec<OrderDauerauftrag> {
    sorted_file
        .order_dauerauftrag
        .iter()
        .map(|l| read_order_dauerauftrag(l.into()))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::diskrepresentation::line::builder::line;
    use crate::model::database::depotwert::builder::depotwert_referenz;
    use crate::model::database::order_dauerauftrag::builder::DEMO_ORDER_DAUERAUFTRAG_AS_DB_STR;
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_vier;
    use crate::model::primitives::datum::builder::datum;
    use crate::model::primitives::name::name;
    use crate::model::primitives::order_betrag::builder::kauf;
    use crate::model::primitives::rhythmus::Rhythmus;

    #[test]
    fn test_read_order() {
        let sorted_file = SortedFile {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparbuchungen: vec![],
            sparkontos: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftrag: vec![line(DEMO_ORDER_DAUERAUFTRAG_AS_DB_STR)],
            depotauszuege: vec![],
        };

        let order_dauerauftraege = read_order_dauerauftraege(&sorted_file);

        let order_dauerauftrag = &order_dauerauftraege[0];
        assert_eq!(order_dauerauftrag.start_datum, datum("2020-01-01"));
        assert_eq!(order_dauerauftrag.ende_datum, datum("2020-01-02"));
        assert_eq!(order_dauerauftrag.rhythmus, Rhythmus::Monatlich);
        assert_eq!(order_dauerauftrag.name, name("MeinName"));
        assert_eq!(order_dauerauftrag.konto, konto_referenz("MeinKonto"));
        assert_eq!(
            order_dauerauftrag.depotwert,
            depotwert_referenz("MeinDepotwert")
        );
        assert_eq!(order_dauerauftrag.wert, kauf(u_vier()));
    }
}
