use crate::budgetbutler::database::select::functions::filters::{
    filter_den_aktuellen_monat, filter_die_letzten_6_monate,
};
use crate::budgetbutler::database::select::functions::grouper::einnahmen_ausgaben_gruppierung;
use crate::budgetbutler::database::select::functions::keyextractors::monatsweise_aggregation;
use crate::budgetbutler::database::select::selector::generate_monats_indizes;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::{Datum, MonatsName};
use crate::model::state::persistent_application_state::Database;

pub struct DashboardViewResult {
    pub zusammenfassung_monatsliste: Vec<MonatsName>,
    pub zusammenfassung_einnahmenliste: Vec<Betrag>,
    pub zusammenfassung_ausgabenliste: Vec<Betrag>,
    pub ausgaben_des_aktuellen_monats: Vec<Indiziert<Einzelbuchung>>,
}

pub struct DashboardContext<'a> {
    pub database: &'a Database,
    pub today: Datum,
}

pub fn handle_view(context: DashboardContext) -> DashboardViewResult {
    let einnahmen_ausgaben = context
        .database
        .einzelbuchungen
        .select()
        .filter(filter_die_letzten_6_monate(context.today.clone()))
        .group_by(monatsweise_aggregation, einnahmen_ausgaben_gruppierung);

    let first_month = context
        .today
        .clone()
        .substract_months(6)
        .clamp_to_first_of_month();
    let mut zusammenfassung_monatsliste = vec![];
    let mut zusammenfassung_einnahmenliste = vec![];
    let mut zusammenfassung_ausgabenliste = vec![];

    for monat in generate_monats_indizes(first_month, context.today.clamp_to_first_of_month()) {
        zusammenfassung_monatsliste.push(monat.format_descriptive_string());
        if let Some(einnahmen_ausgaben) = einnahmen_ausgaben.get(&monat) {
            zusammenfassung_einnahmenliste.push(einnahmen_ausgaben.einnahmen.clone());
            zusammenfassung_ausgabenliste.push(einnahmen_ausgaben.ausgaben.abs());
        } else {
            zusammenfassung_einnahmenliste.push(Betrag::zero());
            zusammenfassung_ausgabenliste.push(Betrag::zero());
        }
    }

    let ausgaben_des_aktuellen_monats = context
        .database
        .einzelbuchungen
        .select()
        .filter(filter_den_aktuellen_monat(context.today.clone()))
        .collect();

    DashboardViewResult {
        zusammenfassung_monatsliste,
        zusammenfassung_einnahmenliste,
        zusammenfassung_ausgabenliste,
        ausgaben_des_aktuellen_monats,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::einzelbuchung::builder::einzelbuchung_with_datum_und_betrag;
    use crate::model::primitives::betrag::builder::{minus_zwei, vier, zwei};
    use crate::model::primitives::datum::monats_name;
    use crate::model::state::persistent_application_state::builder::generate_database_with_einzelbuchungen;

    #[test]
    fn test_handle_view_should_render_graph() {
        let today = Datum::new(01, 01, 2020);
        let database = generate_database_with_einzelbuchungen(vec![
            einzelbuchung_with_datum_und_betrag(today.clone().substract_months(1), zwei()),
            einzelbuchung_with_datum_und_betrag(today.clone().substract_months(1), minus_zwei()),
            einzelbuchung_with_datum_und_betrag(today.clone().substract_months(2), vier()),
            einzelbuchung_with_datum_und_betrag(today.clone().substract_months(3), minus_zwei()),
        ]);
        let context = DashboardContext {
            database: &database,
            today,
        };
        let result = handle_view(context);
        assert_eq!(
            result.zusammenfassung_monatsliste,
            vec![
                monats_name("07/2019"),
                monats_name("08/2019"),
                monats_name("09/2019"),
                monats_name("10/2019"),
                monats_name("11/2019"),
                monats_name("12/2019"),
                monats_name("01/2020")
            ]
        );
        assert_eq!(
            result.zusammenfassung_einnahmenliste,
            vec![
                Betrag::zero(),
                Betrag::zero(),
                Betrag::zero(),
                Betrag::zero(),
                vier(),
                zwei(),
                Betrag::zero()
            ]
        );

        assert_eq!(
            result.zusammenfassung_ausgabenliste,
            vec![
                Betrag::zero(),
                Betrag::zero(),
                Betrag::zero(),
                zwei(),
                Betrag::zero(),
                zwei(),
                Betrag::zero()
            ]
        );
    }

    #[test]
    fn test_handle_view_ausgaben_des_aktuellen_monats() {
        let today = Datum::new(01, 01, 2020);
        let database = generate_database_with_einzelbuchungen(vec![
            einzelbuchung_with_datum_und_betrag(today.clone(), zwei()),
            einzelbuchung_with_datum_und_betrag(today.clone(), minus_zwei()),
            einzelbuchung_with_datum_und_betrag(today.clone().substract_months(1), vier()),
            einzelbuchung_with_datum_und_betrag(today.clone().substract_months(1), minus_zwei()),
        ]);
        let context = DashboardContext {
            database: &database,
            today,
        };

        let result = handle_view(context);

        assert_eq!(result.ausgaben_des_aktuellen_monats.len(), 2);
        assert_eq!(result.ausgaben_des_aktuellen_monats[0].value.betrag, zwei());
        assert_eq!(
            result.ausgaben_des_aktuellen_monats[1].value.betrag,
            minus_zwei()
        );
    }
}
