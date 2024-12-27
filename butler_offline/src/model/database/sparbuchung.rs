use crate::io::disk::database::types::ElementRequirement;
use crate::model::eigenschaften::besitzt_datum::BesitztDatum;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::name::Name;
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SparbuchungTyp {
    ManuelleEinzahlung,
    ManuelleAuszahlung,
    Zinsen,
    Ausschuettung,
    SonstigeKosten,
}

#[derive(Debug, Hash, Clone, PartialEq, Eq)]
pub struct KontoReferenz {
    pub konto_name: Name,
}

impl PartialOrd for KontoReferenz {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for KontoReferenz {
    fn cmp(&self, other: &Self) -> Ordering {
        self.konto_name.cmp(&other.konto_name)
    }
}

impl KontoReferenz {
    pub fn new(konto_name: Name) -> KontoReferenz {
        KontoReferenz { konto_name }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Sparbuchung {
    pub datum: Datum,
    pub name: Name,
    pub wert: BetragOhneVorzeichen,
    pub typ: SparbuchungTyp,
    pub konto: KontoReferenz,
}

impl ElementRequirement for Sparbuchung {}

impl<'a> BesitztDatum<'a> for Sparbuchung {
    fn datum(&'a self) -> &'a Datum {
        &self.datum
    }
}
impl<'a> BesitztDatum<'a> for Indiziert<Sparbuchung> {
    fn datum(&'a self) -> &'a Datum {
        &self.value.datum
    }
}

impl Sparbuchung {
    pub fn new(
        datum: Datum,
        name: Name,
        wert: BetragOhneVorzeichen,
        typ: SparbuchungTyp,
        konto: KontoReferenz,
    ) -> Sparbuchung {
        Sparbuchung {
            datum,
            name,
            wert,
            typ,
            konto,
        }
    }
}

impl PartialOrd<Self> for Sparbuchung {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Sparbuchung {
    fn cmp(&self, other: &Self) -> Ordering {
        let datum_ord = self.datum.cmp(&other.datum);
        if datum_ord != Ordering::Equal {
            return datum_ord;
        }
        self.name.cmp(&other.name)
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::database::sparbuchung::{KontoReferenz, Sparbuchung, SparbuchungTyp};
    use crate::model::primitives::betrag::builder::any_betrag;
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::name::Name;

    pub fn demo_konto_referenz() -> KontoReferenz {
        KontoReferenz {
            konto_name: Name::new("Any Konto Referenz".to_string()),
        }
    }

    pub fn sparbuchung_with_datum(datum: Datum) -> Sparbuchung {
        Sparbuchung {
            datum,
            name: demo_name(),
            wert: any_betrag().unsigned(),
            typ: SparbuchungTyp::ManuelleEinzahlung,
            konto: demo_konto_referenz(),
        }
    }

    pub fn sparbuchung_with_name(name: Name) -> Sparbuchung {
        Sparbuchung {
            datum: any_datum(),
            name,
            wert: any_betrag().unsigned(),
            typ: SparbuchungTyp::ManuelleEinzahlung,
            konto: demo_konto_referenz(),
        }
    }

    pub fn sparbuchung_with_betrag_und_typ(
        betrag: BetragOhneVorzeichen,
        typ: SparbuchungTyp,
    ) -> Sparbuchung {
        Sparbuchung {
            datum: any_datum(),
            name: demo_name(),
            wert: betrag,
            typ,
            konto: demo_konto_referenz(),
        }
    }

    pub fn sparbuchung_with_betrag_typ_und_konto(
        betrag: BetragOhneVorzeichen,
        typ: SparbuchungTyp,
        konto: KontoReferenz,
    ) -> Sparbuchung {
        Sparbuchung {
            datum: any_datum(),
            name: demo_name(),
            wert: betrag,
            typ,
            konto,
        }
    }

    pub fn konto_referenz(name: &str) -> KontoReferenz {
        KontoReferenz::new(Name::new(name.to_string()))
    }

    pub fn any_sparbuchung() -> Sparbuchung {
        Sparbuchung {
            datum: any_datum(),
            name: demo_name(),
            wert: any_betrag().unsigned(),
            typ: SparbuchungTyp::ManuelleEinzahlung,
            konto: demo_konto_referenz(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::builder::sparbuchung_with_datum;
    use super::Datum;
    use crate::model::primitives::name::name;

    #[test]
    fn test_ord_by_datum() {
        let left = sparbuchung_with_datum(Datum::new(2020, 1, 1));
        let right = sparbuchung_with_datum(Datum::new(2020, 1, 2));

        assert!(left < right);
    }

    #[test]
    fn test_ord_by_name() {
        use super::builder::sparbuchung_with_name;
        let left = sparbuchung_with_name(name("A"));
        let right = sparbuchung_with_name(name("B"));

        assert!(left < right);
    }
}
