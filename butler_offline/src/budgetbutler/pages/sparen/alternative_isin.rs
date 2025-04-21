use crate::model::primitives::isin::ISIN;
use crate::model::shares::shares_index::AlternativeISINIndex;

pub struct AlternativeIsin {
    pub isin: ISIN,
    pub isin_alternativen: Vec<IsinAlternative>,
}

pub struct IsinAlternative {
    pub isin: ISIN,
    pub display_name: String,
}

pub fn calculate_alternative_isins(
    index: AlternativeISINIndex,
    current_isin: &ISIN,
) -> AlternativeIsin {
    let mut isin_alternativen: Vec<IsinAlternative> = vec![];

    for entry in index.data {
        let alternative_isin = IsinAlternative {
            isin: entry.isin.clone(),
            display_name: format!(
                "{} ({}, {})",
                entry.index.name, entry.name.name, entry.isin.isin
            ),
        };
        isin_alternativen.push(alternative_isin);
    }

    AlternativeIsin {
        isin: current_isin.clone(),
        isin_alternativen,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::alternative_isin::calculate_alternative_isins;
    use crate::model::primitives::etf_index::builder::etf_index;
    use crate::model::primitives::etf_name::builder::etf_name;
    use crate::model::primitives::isin::builder::isin;
    use crate::model::shares::shares_index::{AlternativeISINIndex, AlternativeISINIndexEntry};

    #[test]
    fn test_calculate_alternative_isins() {
        let index = AlternativeISINIndex {
            data: vec![
                AlternativeISINIndexEntry {
                    isin: isin("DE000A0D9PT0"),
                    name: etf_name("Test ETF"),
                    index: etf_index("Test Index"),
                },
                AlternativeISINIndexEntry {
                    isin: isin("DE000A0D9PT1"),
                    name: etf_name("Test ETF 2"),
                    index: etf_index("Test Index 2"),
                },
            ],
        };

        let current_isin = isin("DE000A0D9PT2");

        let result = calculate_alternative_isins(index, &current_isin);

        assert_eq!(result.isin.isin, current_isin.isin);
        assert_eq!(result.isin_alternativen.len(), 2);

        assert_eq!(result.isin_alternativen[0].isin.isin, "DE000A0D9PT0");
        assert_eq!(
            result.isin_alternativen[0].display_name,
            "Test Index (Test ETF, DE000A0D9PT0)"
        );
        assert_eq!(result.isin_alternativen[1].isin.isin, "DE000A0D9PT1");
        assert_eq!(
            result.isin_alternativen[1].display_name,
            "Test Index 2 (Test ETF 2, DE000A0D9PT1)"
        );
    }
}
