use crate::model::primitives::isin::ISIN;
use crate::model::shares::{Share, ShareState};
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use crate::model::user_data::SHARES_FILE_NAME;
use std::collections::HashMap;
use std::fs;

pub fn load_shares(user_application_directory: &UserApplicationDirectory) -> ShareState {
    eprintln!("Loading shares from: {:?}", user_application_directory);
    if exists_shares(user_application_directory) {
        read_shares(user_application_directory)
    } else {
        eprintln!("No shares found, creating new state");
        ShareState::new()
    }
}

pub fn save_shares(
    user_application_directory: &UserApplicationDirectory,
    share_state: &ShareState,
) {
    eprintln!("Saving shares from: {:?}", user_application_directory);
    let full_path = user_application_directory.path.join(SHARES_FILE_NAME);
    let shares: HashMap<String, Share> = share_state
        .shares
        .iter()
        .map(|(isin, share)| (isin.isin.to_string(), share.clone()))
        .collect();
    let json = serde_json::to_string_pretty(&shares).unwrap();
    fs::write(full_path, json).expect("Could not write shares file");
}

fn exists_shares(user_application_directory: &UserApplicationDirectory) -> bool {
    let full_path = user_application_directory.path.join(SHARES_FILE_NAME);
    full_path.exists()
}

fn read_shares(user_application_directory: &UserApplicationDirectory) -> ShareState {
    let full_path = user_application_directory
        .path
        .join("shares_data.cache.json");
    let file = fs::File::open(full_path).unwrap();
    let shares: HashMap<String, Share> = serde_json::from_reader(file).unwrap();
    ShareState::from(
        shares
            .iter()
            .map(|(isin, share)| (ISIN::new(isin.to_string()), share.clone()))
            .collect(),
    )
}
