use crate::io::disk::database::types::ElementRequirement;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::name::Name;
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DepotwertTyp {
    ETF,
    Fond,
    Einzelaktie,
    Crypto,
    Robot,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Depotwert {
    pub name: Name,
    pub isin: ISIN,
    pub typ: DepotwertTyp,
}

impl DepotwertReferenz {
    pub fn new(isin: ISIN) -> DepotwertReferenz {
        DepotwertReferenz { isin }
    }
}

#[derive(Debug, Hash, Clone, PartialEq, Eq)]
pub struct DepotwertReferenz {
    pub isin: ISIN,
}

impl ElementRequirement for Depotwert {}

impl Depotwert {
    pub fn new(name: Name, isin: ISIN, typ: DepotwertTyp) -> Depotwert {
        Depotwert { name, isin, typ }
    }

    pub fn as_referenz(&self) -> DepotwertReferenz {
        DepotwertReferenz::new(self.isin.clone())
    }
}

impl PartialOrd<Self> for Depotwert {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Depotwert {
    fn cmp(&self, other: &Self) -> Ordering {
        let isin_cmp = self.isin.cmp(&other.isin);
        if isin_cmp != Ordering::Equal {
            return isin_cmp;
        }
        self.name.cmp(&other.name)
    }
}

impl PartialOrd<Self> for DepotwertReferenz {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for DepotwertReferenz {
    fn cmp(&self, other: &Self) -> Ordering {
        self.isin.cmp(&other.isin)
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::database::depotwert::{Depotwert, DepotwertReferenz, DepotwertTyp};
    use crate::model::primitives::isin::builder::{demo_isin, isin};
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::name::name;

    pub fn any_depotwert() -> Depotwert {
        Depotwert::new(demo_name(), demo_isin(), DepotwertTyp::ETF)
    }

    pub fn demo_depotwert_referenz() -> DepotwertReferenz {
        DepotwertReferenz { isin: demo_isin() }
    }

    pub fn depotwert_referenz(isin_: &str) -> DepotwertReferenz {
        DepotwertReferenz { isin: isin(isin_) }
    }

    pub fn depotwert_mit_name(name_str: &str) -> Depotwert {
        Depotwert::new(name(name_str), demo_isin(), DepotwertTyp::ETF)
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::depotwert::{Depotwert, DepotwertTyp};
    use crate::model::primitives::isin::builder::{demo_isin, isin};
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::name::name;
    use std::cmp::Ordering;

    #[test]
    fn test_ord_by_isin() {
        let depotwert1 = Depotwert::new(demo_name(), isin("ISIN1"), DepotwertTyp::ETF);
        let depotwert2 = Depotwert::new(demo_name(), isin("ISIN2"), DepotwertTyp::ETF);

        assert_eq!(depotwert1.cmp(&depotwert2), Ordering::Less);
    }

    #[test]
    fn test_ord_by_name() {
        let depotwert1 = Depotwert::new(name("Name1"), demo_isin(), DepotwertTyp::ETF);
        let depotwert2 = Depotwert::new(name("Name2"), demo_isin(), DepotwertTyp::ETF);

        assert_eq!(depotwert1.cmp(&depotwert2), Ordering::Less);
    }
}
