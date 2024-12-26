use crate::io::disk::database::types::ElementRequirement;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::eigenschaften::besitzt_datum::BesitztDatum;
use crate::model::eigenschaften::besitzt_konto_referenz::BesitztKontoReferenz;
use crate::model::indiziert::Indiziert;
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

impl<'a> BesitztDatum<'a> for Indiziert<Depotauszug> {
    fn datum(&'a self) -> &'a Datum {
        &self.value.datum
    }
}

impl PartialOrd<Self> for Depotauszug {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl<'a> BesitztKontoReferenz<'a> for Indiziert<Depotauszug> {
    fn konto_referenz(&'a self) -> &'a KontoReferenz {
        &self.value.konto
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
    use crate::model::database::depotwert::builder::{demo_depotwert_referenz, depotwert_referenz};
    use crate::model::database::depotwert::DepotwertReferenz;
    use crate::model::database::sparbuchung::builder::{demo_konto_referenz, konto_referenz};
    use crate::model::database::sparbuchung::KontoReferenz;
    use crate::model::primitives::betrag::builder::any_betrag;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::builder::{any_datum, datum};
    use crate::model::primitives::datum::Datum;

    pub fn demo_depotauszug() -> Depotauszug {
        Depotauszug {
            datum: any_datum(),
            depotwert: demo_depotwert_referenz(),
            konto: demo_konto_referenz(),
            wert: any_betrag(),
        }
    }

    pub fn depotauszug_with_datum(datum: Datum) -> Depotauszug {
        Depotauszug {
            datum,
            depotwert: demo_depotwert_referenz(),
            konto: demo_konto_referenz(),
            wert: any_betrag(),
        }
    }

    pub fn depotauszug_with_konto(konto_referenz: KontoReferenz) -> Depotauszug {
        Depotauszug {
            datum: any_datum(),
            depotwert: demo_depotwert_referenz(),
            konto: konto_referenz,
            wert: any_betrag(),
        }
    }

    pub fn depotauszug_with_depotwert(depotwert_referenz: DepotwertReferenz) -> Depotauszug {
        Depotauszug {
            datum: any_datum(),
            depotwert: depotwert_referenz,
            konto: demo_konto_referenz(),
            wert: any_betrag(),
        }
    }

    pub fn depotauszug_with_konto_and_wert(
        konto_referenz: KontoReferenz,
        depotwert_referenz: DepotwertReferenz,
        wert: Betrag,
    ) -> Depotauszug {
        Depotauszug {
            datum: any_datum(),
            depotwert: depotwert_referenz,
            konto: konto_referenz,
            wert,
        }
    }

    pub const DEMO_DEPOTAUSZUG_STR: &str = "2020-01-01,DE000A0D9PT0,MeinKonto,1000.00";

    pub fn demo_depotauszug_aus_str() -> Depotauszug {
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
