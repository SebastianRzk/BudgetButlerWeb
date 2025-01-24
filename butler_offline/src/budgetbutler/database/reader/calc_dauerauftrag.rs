use crate::budgetbutler::database::reader::rhythmus::get_monatsdelta_for_rhythmus;
use crate::model::database::dauerauftrag::Dauerauftrag;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::database::order::Order;
use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
use crate::model::primitives::datum::Datum;
use std::cmp::min;

pub fn calc_dauerauftrag(dauerauftrag: &Dauerauftrag, heute: Datum) -> Vec<Einzelbuchung> {
    let mut lauf_datum = dauerauftrag.start_datum.clone();
    let ende_datum = min(dauerauftrag.ende_datum.clone(), heute);
    let mut buchungen: Vec<Einzelbuchung> = Vec::new();
    let mut monatsdelta = 0;
    while lauf_datum < ende_datum {
        let einzelbuchung = Einzelbuchung {
            datum: lauf_datum.clone(),
            name: dauerauftrag.name.clone(),
            kategorie: dauerauftrag.kategorie.clone(),
            betrag: dauerauftrag.betrag.clone(),
        };
        buchungen.push(einzelbuchung);
        monatsdelta += get_monatsdelta_for_rhythmus(dauerauftrag.rhythmus);
        lauf_datum = dauerauftrag.start_datum.clone().add_months(monatsdelta);
    }
    buchungen
}

pub fn calc_order_dauerauftrag(dauerauftrag: &OrderDauerauftrag, heute: Datum) -> Vec<Order> {
    let mut lauf_datum = dauerauftrag.start_datum.clone();
    let ende_datum = min(dauerauftrag.ende_datum.clone(), heute);
    let mut orders: Vec<Order> = Vec::new();
    while lauf_datum < ende_datum {
        let order = Order {
            datum: lauf_datum.clone(),
            name: dauerauftrag.name.clone(),
            konto: dauerauftrag.konto.clone(),
            depotwert: dauerauftrag.depotwert.clone(),
            wert: dauerauftrag.wert.clone(),
        };
        orders.push(order);

        lauf_datum = lauf_datum.add_months(get_monatsdelta_for_rhythmus(dauerauftrag.rhythmus));
    }
    orders
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::depotwert::builder::depotwert_referenz;
    use crate::model::database::order::OrderTyp::Verkauf;
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::order_betrag::OrderBetrag;
    use crate::model::primitives::rhythmus::Rhythmus;

    #[test]
    fn test_calc_dauerauftrag_monatlich() {
        let dauerauftrag = Dauerauftrag {
            start_datum: Datum::new(1, 1, 2020),
            ende_datum: Datum::new(1, 4, 2020),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 123, 12),
            rhythmus: Rhythmus::Monatlich,
        };

        let result = calc_dauerauftrag(&dauerauftrag, Datum::new(1, 3, 2024));

        assert_eq!(result.len(), 3);
        assert_eq!(result[0].datum, Datum::new(1, 1, 2020));
        assert_eq!(result[1].datum, Datum::new(1, 2, 2020));
        assert_eq!(result[2].datum, Datum::new(1, 3, 2020));
    }

    #[test]
    fn test_calc_dauerauftrag_monatlich_should_clamp_last_of_month() {
        let dauerauftrag = Dauerauftrag {
            start_datum: Datum::new(31, 1, 2020),
            ende_datum: Datum::new(1, 6, 2020),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 123, 12),
            rhythmus: Rhythmus::Monatlich,
        };

        let result = calc_dauerauftrag(&dauerauftrag, Datum::new(1, 3, 2024));

        assert_eq!(result.len(), 5);
        assert_eq!(result[0].datum, Datum::new(31, 1, 2020));
        assert_eq!(result[1].datum, Datum::new(28, 2, 2020));
        assert_eq!(result[2].datum, Datum::new(31, 3, 2020));
        assert_eq!(result[3].datum, Datum::new(30, 4, 2020));
        assert_eq!(result[4].datum, Datum::new(31, 5, 2020));
    }

    #[test]
    fn test_calc_dauerauftrag_vierteljährlich() {
        let dauerauftrag = Dauerauftrag {
            start_datum: Datum::new(1, 1, 2020),
            ende_datum: Datum::new(1, 7, 2020),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 123, 12),
            rhythmus: Rhythmus::Vierteljaehrlich,
        };

        let result = calc_dauerauftrag(&dauerauftrag, Datum::new(1, 3, 2024));

        assert_eq!(result.len(), 2);
        assert_eq!(result[0].datum, Datum::new(1, 1, 2020));
        assert_eq!(result[1].datum, Datum::new(1, 4, 2020));
    }

    #[test]
    fn test_calc_dauerauftrag_should_end_heute_when_endedatum_nach_heute() {
        let dauerauftrag = Dauerauftrag {
            start_datum: Datum::new(1, 1, 2020),
            ende_datum: Datum::new(1, 7, 2020),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 123, 12),
            rhythmus: Rhythmus::Jaehrlich,
        };

        let result = calc_dauerauftrag(&dauerauftrag, Datum::new(1, 3, 2020));

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].datum, Datum::new(1, 1, 2020));
    }

    #[test]
    fn test_calc_order_dauerauftrag_monatlich() {
        let dauerauftrag = OrderDauerauftrag {
            start_datum: Datum::new(1, 1, 2020),
            ende_datum: Datum::new(1, 4, 2020),
            name: name("Normal"),
            konto: konto_referenz("Konto"),
            depotwert: depotwert_referenz("Depotwert"),
            wert: OrderBetrag::new(BetragOhneVorzeichen::new(123, 12), Verkauf),
            rhythmus: Rhythmus::Monatlich,
        };

        let result = calc_order_dauerauftrag(&dauerauftrag, Datum::new(1, 3, 2024));

        assert_eq!(result.len(), 3);
        assert_eq!(result[0].datum, Datum::new(1, 1, 2020));
        assert_eq!(
            result[0].wert,
            OrderBetrag::new(BetragOhneVorzeichen::new(123, 12), Verkauf)
        );
        assert_eq!(result[0].depotwert, depotwert_referenz("Depotwert"));
        assert_eq!(result[0].name, name("Normal"));
        assert_eq!(result[0].konto, konto_referenz("Konto"));

        assert_eq!(result[1].datum, Datum::new(1, 2, 2020));
        assert_eq!(result[2].datum, Datum::new(1, 3, 2020));
    }
}
