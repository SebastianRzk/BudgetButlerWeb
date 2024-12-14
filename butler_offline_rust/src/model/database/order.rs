use crate::io::disk::database::types::ElementRequirement;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::name::Name;
use std::cmp::Ordering;


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Order {
    pub datum: Datum,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwert: DepotwertReferenz,
    pub wert: Betrag,
}

impl ElementRequirement for Order {}

impl Order {
    pub fn new(
        datum: Datum,
        name: Name,
        konto: KontoReferenz,
        depot: DepotwertReferenz,
        wert: Betrag,
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
    use crate::model::database::depotwert::builder::{any_depotwert_referenz, depotwert_referenz};
    use crate::model::database::order::Order;
    use crate::model::database::sparbuchung::builder::{any_konto_referenz, konto_referenz};
    use crate::model::database::sparbuchung::KontoReferenz;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::betrag::builder::{any_betrag, vier};
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::builder::any_name;
    use crate::model::primitives::name::{name, Name};

    pub fn any_order() -> Order {
        Order {
            datum: any_datum(),
            name: any_name(),
            konto: any_konto_referenz(),
            depotwert: any_depotwert_referenz(),
            wert: any_betrag(),
        }
    }

    pub const DEMO_ORDER_AS_DB_STR: &str = "2020-01-01,MeinName,MeinKonto,MeinDepotwert,4.00";

    pub fn demo_order() -> Order {
        Order {
            datum: any_datum(),
            name: name("MeinName"),
            konto: konto_referenz("MeinKonto"),
            depotwert: depotwert_referenz("MeinDepotwert"),
            wert: vier(),
        }
    }

    pub fn order_with_datum(datum: Datum) -> Order {
        Order {
            datum,
            name: any_name(),
            konto: any_konto_referenz(),
            depotwert: any_depotwert_referenz(),
            wert: any_betrag(),
        }
    }

    pub fn order_with_konto(konto: KontoReferenz) -> Order {
        Order {
            datum: any_datum(),
            name: any_name(),
            konto,
            depotwert: any_depotwert_referenz(),
            wert: any_betrag(),
        }
    }

    pub fn order_with_name(name: Name) -> Order {
        Order {
            datum: any_datum(),
            name,
            konto: any_konto_referenz(),
            depotwert: any_depotwert_referenz(),
            wert: any_betrag(),
        }
    }

    pub fn order_with_konto_und_betrag(konto: KontoReferenz, betrag: Betrag) -> Order {
        Order {
            datum: any_datum(),
            name: any_name(),
            konto,
            depotwert: any_depotwert_referenz(),
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
