use crate::model::metamodel::datum_selektion::DatumSelektion;

pub struct DatumTemplate {
    pub can_be_chosen: bool,
    pub datum: String,
    pub datum_german: String,
}

pub fn create_datum_select(data: Vec<DatumSelektion>) -> Vec<DatumTemplate> {
    data.iter()
        .map(|datum| DatumTemplate {
            can_be_chosen: datum.can_be_chosen,
            datum: datum.datum.to_iso_string(),
            datum_german: datum.datum.to_german_string(),
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::create_datum_select;
    use crate::model::metamodel::datum_selektion::DatumSelektion;
    use crate::model::primitives::datum::Datum;

    #[test]
    pub fn test_create_datum_select() {
        let data = vec![
            DatumSelektion {
                datum: Datum::new(1, 1, 2021),
                can_be_chosen: true,
            },
            DatumSelektion {
                datum: Datum::new(01, 02, 2021),
                can_be_chosen: false,
            },
        ];
        let result = create_datum_select(data);
        assert_eq!(result.len(), 2);
        assert_eq!(result[0].can_be_chosen, true);
        assert_eq!(result[0].datum, "2021-01-01");
        assert_eq!(result[0].datum_german, "01.01.2021");
        assert_eq!(result[1].can_be_chosen, false);
        assert_eq!(result[1].datum, "2021-02-01");
        assert_eq!(result[1].datum_german, "01.02.2021");
    }
}
