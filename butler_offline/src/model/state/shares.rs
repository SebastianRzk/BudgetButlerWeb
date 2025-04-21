use crate::model::shares::shares_state::ShareState;
use std::sync::Mutex;

pub struct SharesData {
    pub data: Mutex<ShareState>,
}
