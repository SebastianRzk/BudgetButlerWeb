use crate::model::primitives::datum::Datum;
use crate::model::primitives::etf_index::ETFIndex;
use crate::model::primitives::etf_name::ETFName;
use crate::model::primitives::isin::ISIN;

pub struct SharesIndex {
    pub data: Vec<SharesIndexEntry>,
}

pub struct SharesIndexEntry {
    pub isin: ISIN,
    pub datum: Datum,
}

pub struct AlternativeISINIndex {
    pub data: Vec<AlternativeISINIndexEntry>,
}

pub struct AlternativeISINIndexEntry {
    pub isin: ISIN,
    pub index: ETFIndex,
    pub name: ETFName,
}
