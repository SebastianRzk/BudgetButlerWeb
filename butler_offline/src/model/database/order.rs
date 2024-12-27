use crate::io::disk::database::types::ElementRequirement;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::eigenschaften::besitzt_datum::BesitztDatum;
use crate::model::eigenschaften::besitzt_konto_referenz::BesitztKontoReferenz;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::name::Name;
use crate::model::primitives::order_betrag::OrderBetrag;
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Order {
    pub datum: Datum,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwert: DepotwertReferenz,
    pub wert: OrderBetrag,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum OrderTyp {
    Kauf,
    Verkauf,
    Steuer,
    Dividende,
    SonstigeKosten,
}

impl ElementRequirement for Order {}

impl Order {
    pub fn new(
        datum: Datum,
        name: Name,
        konto: KontoReferenz,
        depot: DepotwertReferenz,
        wert: OrderBetrag,
    ) -> Order {
        Order {
            datum,
            name,
            konto,
            depotwert: depot,
            wert,
        }
    }
}

impl PartialOrd<Self> for Order {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl<'a> BesitztDatum<'a> for Indiziert<Order> {
    fn datum(&'a self) -> &'a Datum {
        &self.value.datum
    }
}

impl<'a> BesitztKontoReferenz<'a> for Indiziert<Order> {
    fn konto_referenz(&'a self) -> &'a KontoReferenz {
        &self.value.konto
    }
}

impl Ord for Order {
    fn cmp(&self, other: &Self) -> Ordering {
        let datum_ord = self.datum.cmp(&other.datum);
        if datum_ord != Ordering::Equal {
            return datum_ord;
        }
        let konto_ord = self.konto.cmp(&other.konto);
        if konto_ord != Ordering::Equal {
            return konto_ord;
        }
        self.name.cmp(&other.name)
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::database::depotwert::builder::{demo_depotwert_referenz, depotwert_referenz};
    use crate::model::database::order::Order;
    use crate::model::database::sparbuchung::builder::{demo_konto_referenz, konto_referenz};
    use crate::model::database::sparbuchung::KontoReferenz;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_vier;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::name::{name, Name};
    use crate::model::primitives::order_betrag::builder::{demo_order_betrag, kauf};
    use crate::model::primitives::order_betrag::OrderBetrag;

    pub fn any_order() -> Order {
        Order {
            datum: any_datum(),
            name: demo_name(),
            konto: demo_konto_referenz(),
            depotwert: demo_depotwert_referenz(),
            wert: demo_order_betrag(),
        }
    }

    pub const DEMO_ORDER_AS_DB_STR: &str = "2020-01-01,MeinName,MeinKonto,MeinDepotwert,4.00,Kauf";

    pub fn demo_order() -> Order {
        Order {
            datum: any_datum(),
            name: name("MeinName"),
            konto: konto_referenz("MeinKonto"),
            depotwert: depotwert_referenz("MeinDepotwert"),
            wert: kauf(u_vier()),
        }
    }

    pub fn order_with_datum(datum: Datum) -> Order {
        Order {
            datum,
            name: demo_name(),
            konto: demo_konto_referenz(),
            depotwert: demo_depotwert_referenz(),
            wert: demo_order_betrag(),
        }
    }

    pub fn order_with_konto(konto: KontoReferenz) -> Order {
        Order {
            datum: any_datum(),
            name: demo_name(),
            konto,
            depotwert: demo_depotwert_referenz(),
            wert: demo_order_betrag(),
        }
    }

    pub fn order_with_name(name: Name) -> Order {
        Order {
            datum: any_datum(),
            name,
            konto: demo_konto_referenz(),
            depotwert: demo_depotwert_referenz(),
            wert: demo_order_betrag(),
        }
    }

    pub fn order_with_konto_und_betrag(konto: KontoReferenz, betrag: OrderBetrag) -> Order {
        Order {
            datum: any_datum(),
            name: demo_name(),
            konto,
            depotwert: demo_depotwert_referenz(),
            wert: betrag,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::builder::{order_with_datum, order_with_konto, order_with_name};
    use super::Datum;
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::primitives::name::name;

    #[test]
    fn test_ord_by_datum() {
        let left = order_with_datum(Datum::new(2020, 1, 1));
        let right = order_with_datum(Datum::new(2020, 1, 2));

        assert!(left < right);
    }

    #[test]
    fn test_ord_by_konto() {
        let left = order_with_konto(konto_referenz("A"));
        let right = order_with_konto(konto_referenz("B"));

        assert!(left < right);
    }

    #[test]
    fn test_ord_by_name() {
        let left = order_with_name(name("A"));
        let right = order_with_name(name("B"));

        assert!(left < right);
    }
}
