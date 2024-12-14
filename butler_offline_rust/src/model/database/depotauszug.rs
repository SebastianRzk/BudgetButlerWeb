use crate::io::disk::database::types::ElementRequirement;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Depotauszug {
    pub datum: Datum,
    pub depotwert: DepotwertReferenz,
    pub konto: KontoReferenz,
    pub wert: Betrag,
}

impl ElementRequirement for Depotauszug {}

impl Depotauszug {
    pub fn new(
        datum: Datum,
        depotwert: DepotwertReferenz,
        konto: KontoReferenz,
        wert: Betrag,
    ) -> Depotauszug {
        Depotauszug {
            datum,
            depotwert,
            konto,
            wert,
        }
    }
}

impl PartialOrd<Self> for Depotauszug {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Depotauszug {
    fn cmp(&self, other: &Self) -> Ordering {
        let datum_ord = self.datum.cmp(&other.datum);
        if datum_ord != Ordering::Equal {
            return datum_ord;
        }
        let konto_ord = self.konto.cmp(&other.konto);
        if konto_ord != Ordering::Equal {
            return konto_ord;
        }
        self.depotwert.cmp(&other.depotwert)
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::database::depotauszug::Depotauszug;
    use crate::model::database::depotwert::builder::{any_depotwert_referenz, depotwert_referenz};
    use crate::model::database::depotwert::DepotwertReferenz;
    use crate::model::database::sparbuchung::builder::{any_konto_referenz, konto_referenz};
    use crate::model::database::sparbuchung::KontoReferenz;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::betrag::builder::any_betrag;
    use crate::model::primitives::datum::builder::{any_datum, datum};
    use crate::model::primitives::datum::Datum;

    pub fn any_depotauszug() -> Depotauszug {
        Depotauszug {
            datum: any_datum(),
            depotwert: any_depotwert_referenz(),
            konto: any_konto_referenz(),
            wert: any_betrag(),
        }
    }

    pub fn depotauszug_with_datum(datum: Datum) -> Depotauszug {
        Depotauszug {
            datum,
            depotwert: any_depotwert_referenz(),
            konto: any_konto_referenz(),
            wert: any_betrag(),
        }
    }

    pub fn depotauszug_with_konto(konto_referenz: KontoReferenz) -> Depotauszug {
        Depotauszug {
            datum: any_datum(),
            depotwert: any_depotwert_referenz(),
            konto: konto_referenz,
            wert: any_betrag(),
        }
    }

    pub fn depotauszug_with_depotwert(depotwert_referenz: DepotwertReferenz) -> Depotauszug {
        Depotauszug {
            datum: any_datum(),
            depotwert: depotwert_referenz,
            konto: any_konto_referenz(),
            wert: any_betrag(),
        }
    }

    pub const DEMO_DEPOTAUSZUG_STR: &str = "2020-01-01,DE000A0D9PT0,MeinKonto,1000.00";

    pub fn demo_depotauszug() -> Depotauszug{
        Depotauszug {
            datum: datum("2020-01-01"),
            depotwert: depotwert_referenz("DE000A0D9PT0"),
            konto: konto_referenz("MeinKonto"),
            wert: Betrag::from_user_input(&"1000,00".to_string()),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::depotauszug::builder::{
        depotauszug_with_datum, depotauszug_with_depotwert, depotauszug_with_konto,
    };
    use crate::model::database::depotwert::builder::depotwert_referenz;
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::primitives::datum::builder::datum;

    #[test]
    fn test_ord_by_datum() {
        let depotauszug1 = depotauszug_with_datum(datum("2020-01-01"));
        let depotauszug2 = depotauszug_with_datum(datum("2020-01-02"));

        assert!(depotauszug1 < depotauszug2);
    }

    #[test]
    fn test_ord_by_konto() {
        let depotauszug1 = depotauszug_with_konto(konto_referenz("konto1"));
        let depotauszug2 = depotauszug_with_konto(konto_referenz("konto2"));

        assert!(depotauszug1 < depotauszug2);
    }

    #[test]
    fn test_ord_by_depotwert() {
        let depotauszug1 = depotauszug_with_depotwert(depotwert_referenz("depotwert1"));
        let depotauszug2 = depotauszug_with_depotwert(depotwert_referenz("depotwert2"));

        assert!(depotauszug1 < depotauszug2);
    }
}
