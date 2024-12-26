use crate::io::disk::database::types::ElementRequirement;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::name::Name;
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Kontotyp {
    Sparkonto,
    GenossenschaftsAnteile,
    Depot,
}

impl ElementRequirement for Sparkonto {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Sparkonto {
    pub name: Name,
    pub kontotyp: Kontotyp,
}

impl Sparkonto {
    pub fn new(name: Name, kontotyp: Kontotyp) -> Sparkonto {
        Sparkonto { name, kontotyp }
    }
}

impl PartialOrd<Self> for Sparkonto {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Sparkonto {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.name.cmp(&other.name)
    }
}

impl Sparkonto {
    pub fn as_reference(&self) -> KontoReferenz {
        KontoReferenz::new(self.name.clone())
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
    use crate::model::primitives::name::builder::demo_name;

    pub fn demo_konto() -> Sparkonto {
        Sparkonto {
            kontotyp: Kontotyp::Depot,
            name: demo_name(),
        }
    }

    pub fn any_konto_with_typ(kontotyp: Kontotyp) -> Sparkonto {
        Sparkonto {
            kontotyp,
            name: demo_name(),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::model::primitives::name::name;

    #[test]
    fn test_ord() {
        use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
        let sparkonto1 = Sparkonto::new(name("Sparkonto1"), Kontotyp::Sparkonto);
        let sparkonto2 = Sparkonto::new(name("Sparkonto2"), Kontotyp::Sparkonto);
        assert!(sparkonto1 < sparkonto2);
    }
}
