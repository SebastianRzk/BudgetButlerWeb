use crate::io::disk::database::order::order_reader::read_order;
use crate::io::disk::diskrepresentation::file::SortedFile;
use crate::model::database::order::Order;

pub fn read_orders(sorted_file: &SortedFile) -> Vec<Order> {
    sorted_file
        .order
        .iter()
        .map(|l| read_order(l.into()))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::diskrepresentation::line::builder::line;
    use crate::model::database::depotwert::builder::depotwert_referenz;
    use crate::model::database::order::OrderTyp::{Kauf, Verkauf};
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::{u_fuenf, u_vier};
    use crate::model::primitives::datum::builder::datum;
    use crate::model::primitives::name::name;
    use crate::model::primitives::order_betrag::OrderBetrag;

    #[test]
    fn test_read_order() {
        let sorted_file = SortedFile {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparbuchungen: vec![],
            sparkontos: vec![],
            depotwerte: vec![],
            order: vec![
                line("2020-01-01,MeinName,MeinKonto,MeinDepotwert,4.00,Kauf"),
                line("2020-01-02,MeinName2,MeinKonto2,MeinDepotwert2,5.00,Verkauf"),
            ],
            order_dauerauftrag: vec![],
            depotauszuege: vec![],
        };

        let orders = read_orders(&sorted_file);

        let order_eins = &orders[0];
        assert_eq!(order_eins.datum, datum("2020-01-01"));
        assert_eq!(order_eins.name, name("MeinName"));
        assert_eq!(order_eins.konto, konto_referenz("MeinKonto"));
        assert_eq!(order_eins.depotwert, depotwert_referenz("MeinDepotwert"));
        assert_eq!(order_eins.wert, OrderBetrag::new(u_vier(), Kauf));

        let order_zwei = &orders[1];
        assert_eq!(order_zwei.datum, datum("2020-01-02"));
        assert_eq!(order_zwei.name, name("MeinName2"));
        assert_eq!(order_zwei.konto, konto_referenz("MeinKonto2"));
        assert_eq!(order_zwei.depotwert, depotwert_referenz("MeinDepotwert2"));
        assert_eq!(order_zwei.wert, OrderBetrag::new(u_fuenf(), Verkauf));
    }
}
