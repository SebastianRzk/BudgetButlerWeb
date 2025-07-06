use crate::model::primitives::datum::Datum;
use crate::model::primitives::isin::ISIN;
use crate::model::shares::shares_state::{Share, ShareDataContent, ShareSnapshot, ShareState};
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use crate::model::user_data::SHARES_FILE_NAME;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;

#[derive(Serialize, Deserialize)]
struct ShareStateOnDisk {
    pub shares: HashMap<ISIN, ShareOnDisk>,
}

#[derive(Serialize, Deserialize, Clone)]
struct ShareOnDisk {
    pub data: Vec<ShareSnapshotOnDisk>,
}

#[derive(Serialize, Deserialize, Clone, PartialEq, Debug)]
struct ShareSnapshotOnDisk {
    pub datum: String,
    pub source: String,
    pub data: ShareDataContentOnDisk,
}

#[derive(Serialize, Deserialize, Clone, PartialEq, Debug)]
struct ShareDataContentOnDisk {
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

    #[serde(rename(
        serialize = "Nachhaltigkeitskriterium",
        deserialize = "Nachhaltigkeitskriterium"
    ))]
    pub nachhaltigkeitskriterium: Option<String>,
}

impl From<ShareDataContentOnDisk> for ShareDataContent {
    fn from(val: ShareDataContentOnDisk) -> Self {
        ShareDataContent {
            name: val.name,
            index_name: val.index_name,
            kosten: val.kosten,
            nachhaltigkeitskriterium: val.nachhaltigkeitskriterium,
            regionen: val.regionen,
            sektoren: val.sektoren,
        }
    }
}

impl From<ShareDataContent> for ShareDataContentOnDisk {
    fn from(data: ShareDataContent) -> Self {
        ShareDataContentOnDisk {
            name: data.name,
            index_name: data.index_name,
            kosten: data.kosten,
            regionen: data.regionen,
            sektoren: data.sektoren,
            nachhaltigkeitskriterium: data.nachhaltigkeitskriterium,
        }
    }
}

impl From<ShareSnapshotOnDisk> for ShareSnapshot {
    fn from(val: ShareSnapshotOnDisk) -> Self {
        ShareSnapshot {
            datum: Datum::from_iso_string(&val.datum),
            source: val.source,
            data: val.data.into(),
        }
    }
}

impl From<ShareSnapshot> for ShareSnapshotOnDisk {
    fn from(data: ShareSnapshot) -> Self {
        ShareSnapshotOnDisk {
            datum: data.datum.to_iso_string(),
            source: data.source,
            data: data.data.into(),
        }
    }
}

impl From<ShareOnDisk> for Share {
    fn from(val: ShareOnDisk) -> Self {
        Share {
            data: val.data.into_iter().map(|s| s.into()).collect(),
        }
    }
}

impl From<Share> for ShareOnDisk {
    fn from(data: Share) -> Self {
        ShareOnDisk {
            data: data.data.into_iter().map(|s| s.into()).collect(),
        }
    }
}

pub fn load_shares(user_application_directory: &UserApplicationDirectory) -> ShareState {
    eprintln!("Loading shares from: {user_application_directory:?}");
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
    eprintln!("Saving shares to: {user_application_directory:?}");
    let full_path = user_application_directory.path.join(SHARES_FILE_NAME);
    let shares: HashMap<String, ShareOnDisk> = share_state
        .shares
        .iter()
        .map(|(isin, share)| (isin.isin.to_string(), share.clone().into()))
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
    let shares: HashMap<String, ShareOnDisk> = serde_json::from_reader(file).unwrap();
    ShareState::from(
        shares
            .into_iter()
            .map(|(isin, share)| (ISIN::new(isin.to_string()), share.into()))
            .collect(),
    )
}
