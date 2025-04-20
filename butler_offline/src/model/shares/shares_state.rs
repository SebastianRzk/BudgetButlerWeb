use crate::model::primitives::datum::Datum;
use crate::model::primitives::isin::ISIN;
use std::collections::HashMap;

pub struct ShareState {
    pub shares: HashMap<ISIN, Share>,
}

impl Default for ShareState {
    fn default() -> Self {
        Self::new()
    }
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

    pub fn get_share(&self, isin: &ISIN) -> Option<&ShareSnapshot> {
        self.shares.get(isin).and_then(|x| x.data.last())
    }

    #[cfg(test)]
    pub fn get_share_data(&self, isin: &ISIN) -> Option<&Vec<ShareSnapshot>> {
        self.shares.get(isin).map(|x| &x.data)
    }

    pub fn append(&mut self, isin: &ISIN, share: ShareSnapshot) {
        if let Some(existing_share) = self.shares.get_mut(isin) {
            existing_share.data.push(share);
        } else {
            self.shares
                .insert(isin.clone(), Share { data: vec![share] });
        }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub struct Share {
    pub data: Vec<ShareSnapshot>,
}

#[derive(Clone, Debug, PartialEq)]
pub struct ShareSnapshot {
    pub datum: Datum,
    pub source: String,
    pub data: ShareDataContent,
}

#[derive(Clone, Debug, PartialEq)]
pub struct ShareDataContent {
    pub name: String,

    pub index_name: String,

    pub kosten: f64,

    pub nachhaltigkeitskriterium: Option<String>,

    pub regionen: HashMap<String, f64>,

    pub sektoren: HashMap<String, f64>,
}

#[cfg(test)]
pub mod builder {
    use crate::model::primitives::datum::Datum;
    use crate::model::shares::shares_state::{ShareDataContent, ShareSnapshot};

    pub fn share_data_mit_kosten(kosten: f64) -> ShareSnapshot {
        ShareSnapshot {
            datum: Datum::first(),
            source: "".to_string(),
            data: ShareDataContent {
                name: "".to_string(),
                index_name: "".to_string(),
                nachhaltigkeitskriterium: None,
                kosten,
                regionen: std::collections::HashMap::new(),
                sektoren: std::collections::HashMap::new(),
            },
        }
    }
}

#[cfg(test)]
mod tests {
    use super::builder::share_data_mit_kosten;
    use super::ShareState;
    use crate::model::primitives::isin::builder::isin;
    use crate::model::shares::shares_state::Share;
    use std::collections::HashMap;

    #[test]
    fn should_return_none_on_missing_share() {
        let state = ShareState::new();
        let isin = crate::model::primitives::isin::ISIN::new("DE000A0D9PT0".to_string());
        assert!(state.get_share(&isin).is_none());
    }

    #[test]
    fn should_return_none_on_empty_data() {
        let mut shares = HashMap::new();
        shares.insert(isin("isin"), Share { data: vec![] });
        let state = ShareState { shares };
        assert!(state.get_share(&isin("isin")).is_none());
    }

    #[test]
    fn test_append_for_non_existent_share_should_add_share() {
        let mut state = ShareState::new();
        let isin = isin("DE000A0D9PT0");
        let share = share_data_mit_kosten(1.0);

        state.append(&isin, share.clone());

        assert_eq!(state.shares.len(), 1);
        assert_eq!(state.get_share_data(&isin).unwrap()[0], share);
    }

    #[test]
    fn test_append_for_existent_share_should_add_new_data() {
        let mut state = ShareState::new();
        let isin = isin("DE000A0D9PT0");
        let share1 = share_data_mit_kosten(1.0);
        let share2 = share_data_mit_kosten(2.0);

        state.append(&isin, share1.clone());
        state.append(&isin, share2.clone());

        assert_eq!(state.shares.len(), 1);
        assert_eq!(state.get_share_data(&isin).unwrap().len(), 2);
        assert_eq!(state.get_share_data(&isin).unwrap()[0], share1);
        assert_eq!(state.get_share_data(&isin).unwrap()[1], share2);
    }
}
