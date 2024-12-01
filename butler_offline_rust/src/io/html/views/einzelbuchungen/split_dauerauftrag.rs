use crate::budgetbutler::pages::einzelbuchungen::split_dauerauftrag::SplitDauerauftragViewResult;
pub use askama::Template;

#[derive(Template)]
#[template(path = "einzelbuchungen/split_dauerauftrag.html")]
pub struct SplitDauerauftragTemplate {
    pub database_id: String,
    pub dauerauftrag_id: String,
    pub datum: Vec<DatumTemplate>,
    pub wert: String,
}

pub struct DatumTemplate {
    pub can_be_chosen: bool,
    pub datum: String,
    pub datum_german: String,
}

pub fn render_split_dauerauftrag_template(template: SplitDauerauftragViewResult) -> String {
    let as_template: SplitDauerauftragTemplate = map_to_template(template);
    as_template.render().unwrap()
}


pub fn map_to_template(view_result: SplitDauerauftragViewResult) -> SplitDauerauftragTemplate {
    SplitDauerauftragTemplate {
        database_id: view_result.database_version.as_string(),
        dauerauftrag_id: view_result.dauerauftrag_id.to_string(),
        wert: view_result.wert.to_german_string(),
        datum: view_result.datum.iter().map(|datum| {
            DatumTemplate {
                can_be_chosen: datum.can_be_chosen,
                datum: datum.datum.to_iso_string(),
                datum_german: datum.datum.to_german_string(),
            }
        }).collect(),
    }
}


#[cfg(test)]
mod tests {
    use super::map_to_template;
    use crate::budgetbutler::pages::einzelbuchungen::split_dauerauftrag::{DatumSelektion, SplitDauerauftragViewResult};
    use crate::model::primitives::betrag::builder::zwei;
    use crate::model::primitives::datum::Datum;
    use crate::model::state::persistent_application_state::builder::empty_database_version;

    #[test]
    pub fn test_map_to_template() {
        let view_result = SplitDauerauftragViewResult {
            database_version: empty_database_version(),
            dauerauftrag_id: 1,
            wert: zwei(),
            datum: vec![
                DatumSelektion {
                    datum: Datum::new(1, 1, 2021),
                    can_be_chosen: true,
                },
                DatumSelektion {
                    datum: Datum::new(01, 02, 2021),
                    can_be_chosen: false,
                },
            ],
        };

        let template = map_to_template(view_result);

        assert_eq!(template.database_id, empty_database_version().as_string());
        assert_eq!(template.dauerauftrag_id, "1");
        assert_eq!(template.wert, "2,00");
        assert_eq!(template.datum.len(), 2);
        assert_eq!(template.datum[0].can_be_chosen, true);
        assert_eq!(template.datum[0].datum, "2021-01-01");
        assert_eq!(template.datum[0].datum_german, "01.01.2021");
        assert_eq!(template.datum[1].can_be_chosen, false);
        assert_eq!(template.datum[1].datum, "2021-02-01");
        assert_eq!(template.datum[1].datum_german, "01.02.2021");
    }
}