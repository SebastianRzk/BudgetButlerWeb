use crate::model::primitives::isin::ISIN;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Serialize, Deserialize)]
pub struct ShareState {
    shares: HashMap<ISIN, Share>,
}

impl ShareState {
    pub fn new() -> ShareState {
        ShareState {
            shares: HashMap::new(),
        }
    }

    pub fn from(shares: HashMap<ISIN, Share>) -> ShareState {
        ShareState { shares }
    }

    pub fn get_share(&self, isin: ISIN) -> Option<&ShareData> {
        self.shares.get(&isin).map(|x| x.data.first()).flatten()
    }
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Share {
    data: Vec<ShareData>,
}

#[derive(Serialize, Deserialize, Clone)]
pub struct ShareData {
    pub date: String,
    pub source: String,
    pub data: ShareDataContent,
}

#[derive(Serialize, Deserialize, Clone)]
pub struct ShareDataContent {
    #[serde(rename(serialize = "Name", deserialize = "Name"))]
    pub name: String,

    #[serde(rename(serialize = "IndexName", deserialize = "IndexName"))]
    pub index_name: String,

    #[serde(rename(serialize = "Kosten", deserialize = "Kosten"))]
    pub kosten: f64,

    #[serde(rename(serialize = "Regionen", deserialize = "Regionen"))]
    pub regionen: HashMap<String, f64>,

    #[serde(rename(serialize = "Sektoren", deserialize = "Sektoren"))]
    pub sektoren: HashMap<String, f64>,
}

#[cfg(test)]
pub mod builder {
    use crate::model::shares::ShareData;

    pub fn share_data_mit_kosten(kosten: f64) -> ShareData {
        ShareData {
            date: "".to_string(),
            source: "".to_string(),
            data: crate::model::shares::ShareDataContent {
                name: "".to_string(),
                index_name: "".to_string(),
                kosten,
                regionen: std::collections::HashMap::new(),
                sektoren: std::collections::HashMap::new(),
            },
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::model::primitives::isin::builder::isin;
    use crate::model::shares::Share;
    use std::collections::HashMap;

    #[test]
    fn should_return_none_on_missing_share() {
        let state = super::ShareState::new();
        let isin = crate::model::primitives::isin::ISIN::new("DE000A0D9PT0".to_string());
        assert_eq!(state.get_share(isin).is_none(), true);
    }

    #[test]
    fn should_return_none_on_empty_data() {
        let mut shares = HashMap::new();
        shares.insert(isin("isin"), Share { data: vec![] });
        let state = super::ShareState { shares };
        assert_eq!(state.get_share(isin("isin")).is_none(), true);
    }
}
