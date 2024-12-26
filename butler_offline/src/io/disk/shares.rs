use crate::model::primitives::isin::ISIN;
use crate::model::shares::{Share, ShareState};
use std::collections::HashMap;
use std::path::PathBuf;

pub fn load_shares(base_path: &PathBuf) -> ShareState {
    eprintln!("Loading shares from: {:?}", base_path);
    if exists_shares(base_path) {
        read_shares(base_path)
    } else {
        eprintln!("No shares found, creating new state");
        ShareState::new()
    }
}

fn exists_shares(base_path: &PathBuf) -> bool {
    let full_path = base_path.join("shares_data.cache.json");
    full_path.exists()
}

fn read_shares(base_path: &PathBuf) -> ShareState {
    let full_path = base_path.join("shares_data.cache.json");
    let file = std::fs::File::open(full_path).unwrap();
    let shares: HashMap<String, Share> = serde_json::from_reader(file).unwrap();
    ShareState::from(
        shares
            .iter()
            .map(|(isin, share)| (ISIN::new(isin.to_string()), share.clone()))
            .collect(),
    )
}
