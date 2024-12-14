use crate::io::disk::database::types::ElementRequirement;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::name::Name;
use crate::model::primitives::rhythmus::Rhythmus;
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OrderDauerauftrag {
    pub start_datum: Datum,
    pub ende_datum: Datum,
    pub rhythmus: Rhythmus,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwert: DepotwertReferenz,
    pub wert: Betrag,
}

impl ElementRequirement for OrderDauerauftrag {}

impl OrderDauerauftrag {
    pub fn new(
        start_datum: Datum,
        ende_datum: Datum,
        rhythmus: Rhythmus,
        name: Name,
        konto: KontoReferenz,
        depotwert: DepotwertReferenz,
        wert: Betrag,
    ) -> OrderDauerauftrag {
        OrderDauerauftrag {
            start_datum,
            ende_datum,
            rhythmus,
            name,
            konto,
            depotwert,
            wert,
        }
    }
}

impl PartialOrd<Self> for OrderDauerauftrag {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for OrderDauerauftrag {
    fn cmp(&self, other: &Self) -> Ordering {
        let start_datum_ord = self.start_datum.cmp(&other.start_datum);
        if start_datum_ord != Ordering::Equal {
            return start_datum_ord;
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
    use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
    use crate::model::database::sparbuchung::builder::{any_konto_referenz, konto_referenz};
    use crate::model::database::sparbuchung::KontoReferenz;
    use crate::model::primitives::betrag::builder::{any_betrag, vier};
    use crate::model::primitives::datum::builder::{any_datum, datum};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::builder::any_name;
    use crate::model::primitives::name::{name, Name};
    use crate::model::primitives::rhythmus::Rhythmus;

    pub fn any_order_dauerauftrag() -> OrderDauerauftrag {
        OrderDauerauftrag {
            start_datum: any_datum(),
            ende_datum: any_datum(),
            rhythmus: Rhythmus::Vierteljaehrlich,
            name: any_name(),
            konto: any_konto_referenz(),
            depotwert: any_depotwert_referenz(),
            wert: any_betrag(),
        }
    }

    pub const DEMO_ORDER_DAUERAUFTRAG_AS_DB_STR: &str =
        "2020-01-01,2020-01-02,monatlich,MeinName,MeinKonto,MeinDepotwert,4.00";

    pub fn demo_order_dauerauftrag() -> OrderDauerauftrag {
        OrderDauerauftrag {
            start_datum: datum("2020-01-01"),
            ende_datum: datum("2020-01-02"),
            rhythmus: Rhythmus::Monatlich,
            name: name("MeinName"),
            konto: konto_referenz("MeinKonto"),
            depotwert: depotwert_referenz("MeinDepotwert"),
            wert: vier(),
        }
    }

    pub fn order_dauerauftrag_with_startdatum(datum: Datum) -> OrderDauerauftrag {
        order_dauerauftrag_with_range(datum.clone(), datum, Rhythmus::Vierteljaehrlich)
    }

    pub fn order_dauerauftrag_with_range(start_datum: Datum, ende_datum: Datum, rhythmus: Rhythmus) -> OrderDauerauftrag {
        OrderDauerauftrag {
            start_datum,
            ende_datum,
            rhythmus,
            name: any_name(),
            konto: any_konto_referenz(),
            depotwert: any_depotwert_referenz(),
            wert: any_betrag(),
        }
    }

    pub fn order_dauerauftrag_with_konto(konto: KontoReferenz) -> OrderDauerauftrag {
        OrderDauerauftrag {
            start_datum: any_datum(),
            ende_datum: any_datum(),
            rhythmus: Rhythmus::Vierteljaehrlich,
            name: any_name(),
            konto,
            depotwert: any_depotwert_referenz(),
            wert: any_betrag(),
        }
    }

    pub fn order_dauerauftrag_with_name(name: Name) -> OrderDauerauftrag {
        OrderDauerauftrag {
            start_datum: any_datum(),
            ende_datum: any_datum(),
            rhythmus: Rhythmus::Vierteljaehrlich,
            name,
            konto: any_konto_referenz(),
            depotwert: any_depotwert_referenz(),
            wert: any_betrag(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::builder::{
        order_dauerauftrag_with_konto, order_dauerauftrag_with_name,
        order_dauerauftrag_with_startdatum,
    };
    use super::Datum;
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::primitives::name::name;

    #[test]
    fn test_ord_by_datum() {
        let left = order_dauerauftrag_with_startdatum(Datum::new(2020, 1, 1));
        let right = order_dauerauftrag_with_startdatum(Datum::new(2020, 1, 2));

        assert!(left < right);
    }

    #[test]
    fn test_ord_by_konto() {
        let left = order_dauerauftrag_with_konto(konto_referenz("A"));
        let right = order_dauerauftrag_with_konto(konto_referenz("B"));

        assert!(left < right);
    }

    #[test]
    fn test_ord_by_name() {
        let left = order_dauerauftrag_with_name(name("A"));
        let right = order_dauerauftrag_with_name(name("B"));

        assert!(left < right);
    }
}
