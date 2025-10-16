use crate::io::online::request::get_request;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::etf_index::ETFIndex;
use crate::model::primitives::etf_name::ETFName;
use crate::model::primitives::isin::ISIN;
use crate::model::shares::shares_index::{
    AlternativeISINIndex, AlternativeISINIndexEntry, SharesIndex, SharesIndexEntry,
};
use crate::model::shares::shares_state::{ShareDataContent, ShareSnapshot};
use serde::Deserialize;
use std::collections::HashMap;

const SHARES_INDEX_URL: &str = "https://raw.githubusercontent.com/SebastianRzk/BudgetButlerWeb-ISIN-Data/refs/heads/master/data/index.json";
const SHARES_ALTERNATIVE_INDEX_URL: &str = "https://raw.githubusercontent.com/SebastianRzk/BudgetButlerWeb-ISIN-Data/refs/heads/master/data/index-alternative.json";
const SHARE_URL: &str = "https://raw.githubusercontent.com/SebastianRzk/BudgetButlerWeb-ISIN-Data/refs/heads/master/data/";

#[derive(Deserialize)]
pub struct SharesIndexEntryDto {
    pub isin: String,
    pub last_modified: String,
}

#[derive(Deserialize)]
pub struct AlternativeISINIndexEntryDto {
    pub isin: String,
    pub referenced_index: String,
    pub name: String,
}

#[derive(Deserialize, Clone, PartialEq, Debug)]
pub struct ShareSnapshotDto {
    pub datum: String,
    pub source: String,
    pub data: ShareDataContentDto,
}

#[derive(Deserialize, Clone, PartialEq, Debug)]
pub struct ShareDataContentDto {
    #[serde(rename(deserialize = "Name"))]
    pub name: String,

    #[serde(rename(deserialize = "IndexName"))]
    pub index_name: String,

    #[serde(rename(deserialize = "Kosten"))]
    pub kosten: f64,

    #[serde(rename(deserialize = "Regionen"))]
    pub regionen: HashMap<String, f64>,

    #[serde(rename(deserialize = "Sektoren"))]
    pub sektoren: HashMap<String, f64>,

    #[serde(rename(deserialize = "Nachhaltigkeitskriterium"))]
    pub nachhaltigkeitskriterium: Option<String>,
}

pub async fn load_shares_index() -> Option<SharesIndex> {
    let response = get_request(SHARES_INDEX_URL).await;

    if let Ok(response) = response {
        let result_content = response;
        let result = serde_json::from_str::<Vec<SharesIndexEntryDto>>(&result_content);
        println!("{:?}", result.err());
        println!("{result_content}");
        println!("{}", result_content.get(0..0).unwrap());
        let result = serde_json::from_str::<Vec<SharesIndexEntryDto>>(&result_content);
        result.ok().map(|dto| SharesIndex {
            data: dto
                .into_iter()
                .map(|entry| SharesIndexEntry {
                    isin: ISIN::new(entry.isin),
                    datum: Datum::from_iso_string(&entry.last_modified),
                })
                .collect(),
        })
    } else {
        None
    }
}

pub async fn load_alternative_isin_index() -> Option<AlternativeISINIndex> {
    let response = get_request(SHARES_ALTERNATIVE_INDEX_URL).await;
    println!(
        "{:?}",
        serde_json::from_str::<Vec<AlternativeISINIndexEntryDto>>(
            &get_request(SHARES_ALTERNATIVE_INDEX_URL).await.unwrap()
        )
        .err()
    );
    if let Ok(response) = response {
        serde_json::from_str::<Vec<AlternativeISINIndexEntryDto>>(&response)
            .ok()
            .map(|dto| AlternativeISINIndex {
                data: dto
                    .into_iter()
                    .map(|entry| AlternativeISINIndexEntry {
                        isin: ISIN::new(entry.isin),
                        index: ETFIndex {
                            name: entry.referenced_index,
                        },
                        name: ETFName { name: entry.name },
                    })
                    .collect(),
            })
    } else {
        None
    }
}

pub async fn fetch_latest_share_data(isin: &ISIN) -> Option<ShareSnapshot> {
    let share_text = get_request(format!("{}latest/{}.json", SHARE_URL, isin.isin).as_str()).await;

    if let Ok(text) = share_text {
        let share_data: ShareSnapshotDto = serde_json::from_str(&text).unwrap();
        Some(ShareSnapshot {
            datum: Datum::from_iso_string(share_data.datum.as_str()),
            source: share_data.source,
            data: ShareDataContent {
                name: share_data.data.name,
                index_name: share_data.data.index_name,
                kosten: share_data.data.kosten,
                regionen: share_data.data.regionen,
                sektoren: share_data.data.sektoren,
                nachhaltigkeitskriterium: share_data.data.nachhaltigkeitskriterium,
            },
        })
    } else {
        None
    }
}
