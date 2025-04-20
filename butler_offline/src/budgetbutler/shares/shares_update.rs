use crate::model::primitives::datum::Datum;
use crate::model::primitives::isin::ISIN;
use crate::model::shares::shares_index::SharesIndex;

#[derive(Debug, PartialEq, Eq)]
pub enum SharesUpdateStatus {
    UpdateAvailable,
    ErrorOnUpdate,
    NoUpdateNeeded,
    NotFound,
}

pub fn calculate_if_share_can_be_updated(
    shares_index: &Option<SharesIndex>,
    requested_update: &ISIN,
    last_update: Option<&Datum>,
) -> SharesUpdateStatus {
    let vergleichs_datum = last_update.cloned().unwrap_or(Datum::first());
    if let Some(index) = shares_index {
        if index
            .data
            .iter()
            .any(|entry| &entry.isin == requested_update && entry.datum > vergleichs_datum)
        {
            SharesUpdateStatus::UpdateAvailable
        } else {
            SharesUpdateStatus::NotFound
        }
    } else {
        SharesUpdateStatus::ErrorOnUpdate
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::shares::shares_update::SharesUpdateStatus;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::isin::builder::demo_isin;
    use crate::model::shares::shares_index::{SharesIndex, SharesIndexEntry};

    #[test]
    fn calculate_if_share_can_be_updated_with_missing_index_should_return_error() {
        let shares_index = None;
        let requested_update = demo_isin();
        let result =
            super::calculate_if_share_can_be_updated(&shares_index, &requested_update, None);
        assert_eq!(result, SharesUpdateStatus::ErrorOnUpdate);
    }

    #[test]
    fn calculate_if_share_can_be_updated_with_not_found_should_return_not_found() {
        let shares_index = Some(SharesIndex { data: vec![] });
        let requested_update = demo_isin();
        let result =
            super::calculate_if_share_can_be_updated(&shares_index, &requested_update, None);
        assert_eq!(result, SharesUpdateStatus::NotFound);
    }

    #[test]
    fn calculate_if_share_can_be_updated_with_found_element_and_datum_not_exists() {
        let shares_index = Some(SharesIndex {
            data: vec![SharesIndexEntry {
                isin: demo_isin(),
                datum: Datum::new(1, 1, 1999),
            }],
        });
        let requested_update = demo_isin();
        let result =
            super::calculate_if_share_can_be_updated(&shares_index, &requested_update, None);
        assert_eq!(result, SharesUpdateStatus::UpdateAvailable);
    }

    #[test]
    fn calculate_if_share_can_be_updated_with_found_element_and_datum_exists_older_index() {
        let shares_index = Some(SharesIndex {
            data: vec![SharesIndexEntry {
                isin: demo_isin(),
                datum: Datum::new(1, 1, 2000),
            }],
        });
        let requested_update = demo_isin();
        let result = super::calculate_if_share_can_be_updated(
            &shares_index,
            &requested_update,
            Some(&Datum::new(1, 1, 1999)),
        );
        assert_eq!(result, SharesUpdateStatus::UpdateAvailable);
    }
    #[test]
    fn calculate_if_share_can_be_updated_with_found_element_and_datum_equals_index_should_return_no_update(
    ) {
        let shares_index = Some(SharesIndex {
            data: vec![SharesIndexEntry {
                isin: demo_isin(),
                datum: Datum::new(1, 1, 2000),
            }],
        });
        let requested_update = demo_isin();
        let result = super::calculate_if_share_can_be_updated(
            &shares_index,
            &requested_update,
            Some(&Datum::new(1, 1, 2000)),
        );
        assert_eq!(result, SharesUpdateStatus::NotFound);
    }
}
