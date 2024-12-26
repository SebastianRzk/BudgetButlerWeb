use crate::budgetbutler::pages::sparen::split_order_dauerauftrag::SplitOrderDauerauftragViewResult;
use crate::io::html::views::templates::datum_renderer::{create_datum_select, DatumTemplate};
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/split_orderdauerauftrag.html")]
pub struct SplitOrderDauerauftragTemplate {
    pub database_version: String,
    pub orderdauerauftrag_id: String,
    pub datum: Vec<DatumTemplate>,
    pub wert: String,
}

pub fn render_split_order_dauerauftrag_template(
    template: SplitOrderDauerauftragViewResult,
) -> String {
    let as_template: SplitOrderDauerauftragTemplate = map_to_template(template);
    as_template.render().unwrap()
}

pub fn map_to_template(
    view_result: SplitOrderDauerauftragViewResult,
) -> SplitOrderDauerauftragTemplate {
    SplitOrderDauerauftragTemplate {
        database_version: view_result.database_version.as_string(),
        orderdauerauftrag_id: view_result.order_dauerauftrag_id.to_string(),
        wert: view_result.wert.to_german_string(),
        datum: create_datum_select(view_result.datum),
    }
}

#[cfg(test)]
mod tests {
    use super::map_to_template;
    use crate::budgetbutler::pages::sparen::split_order_dauerauftrag::SplitOrderDauerauftragViewResult;
    use crate::model::metamodel::datum_selektion::builder::{
        demo_datum_selektion_1, demo_datum_selektion_2,
    };
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::state::persistent_application_state::builder::demo_database_version;

    #[test]
    pub fn test_map_to_template() {
        let view_result = SplitOrderDauerauftragViewResult {
            database_version: demo_database_version(),
            order_dauerauftrag_id: 1,
            wert: u_zwei(),
            datum: vec![demo_datum_selektion_1(), demo_datum_selektion_2()],
        };

        let template = map_to_template(view_result);

        assert_eq!(
            template.database_version,
            demo_database_version().as_string()
        );
        assert_eq!(template.orderdauerauftrag_id, "1");
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
