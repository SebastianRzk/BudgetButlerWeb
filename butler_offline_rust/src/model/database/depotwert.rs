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


impl DepotwertReferenz{
    pub fn new(isin: ISIN) -> DepotwertReferenz {
        DepotwertReferenz { isin }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DepotwertReferenz {
    pub isin: ISIN,
}


impl ElementRequirement for Depotwert{}

impl Depotwert {
    pub fn new(name: Name, isin: ISIN, typ: DepotwertTyp) -> Depotwert {
        Depotwert { name, isin, typ }
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
    use crate::model::primitives::isin::builder::{any_isin, isin};
    use crate::model::primitives::name::builder::any_name;

    pub fn any_depotwert() -> Depotwert {
        Depotwert::new(any_name(), any_isin(), DepotwertTyp::ETF)
    }

    pub fn any_depotwert_referenz() -> DepotwertReferenz {
        DepotwertReferenz {
            isin: any_isin(),
        }
    }

    pub fn depotwert_referenz(isin_: &str) -> DepotwertReferenz {
        DepotwertReferenz {
            isin: isin(isin_),
        }
    }

}

#[cfg(test)]
mod tests {
    use crate::model::database::depotwert::{Depotwert, DepotwertTyp};
    use crate::model::primitives::isin::builder::{any_isin, isin};
    use crate::model::primitives::name::builder::any_name;
    use crate::model::primitives::name::name;
    use std::cmp::Ordering;

    #[test]
    fn test_ord_by_isin() {
        let depotwert1 = Depotwert::new(any_name(), isin("ISIN1"), DepotwertTyp::ETF);
        let depotwert2 = Depotwert::new(any_name(), isin("ISIN2"), DepotwertTyp::ETF);

        assert_eq!(depotwert1.cmp(&depotwert2), Ordering::Less);
    }

    #[test]
    fn test_ord_by_name() {
        let depotwert1 = Depotwert::new(name("Name1"), any_isin(), DepotwertTyp::ETF);
        let depotwert2 = Depotwert::new(name("Name2"), any_isin(), DepotwertTyp::ETF);

        assert_eq!(depotwert1.cmp(&depotwert2), Ordering::Less);
    }
}
