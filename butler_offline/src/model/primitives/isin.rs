use serde::{Deserialize, Serialize};
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Hash, Eq, Serialize, Deserialize)]
pub struct ISIN {
    pub isin: String,
}

impl ISIN {
    pub fn new(isin: String) -> ISIN {
        ISIN { isin }
    }

    pub fn empty() -> ISIN {
        ISIN {
            isin: "".to_string(),
        }
    }
}

impl PartialOrd for ISIN {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for ISIN {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.isin.cmp(&other.isin)
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::primitives::isin::ISIN;

    pub fn isin(isin: &str) -> ISIN {
        ISIN::new(isin.to_string())
    }

    pub fn demo_isin() -> ISIN {
        isin("TestISIN")
    }
}
