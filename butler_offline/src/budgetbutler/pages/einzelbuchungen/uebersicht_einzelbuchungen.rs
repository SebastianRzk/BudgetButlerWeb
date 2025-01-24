use crate::budgetbutler::database::select::functions::datatypes::MonatsAggregationsIndex;
use crate::budgetbutler::database::select::functions::filters::filter_auf_das_jahr;
use crate::budgetbutler::database::select::functions::keyextractors::{
    jahresweise_aggregation, monatsweise_aggregation,
};
use crate::budgetbutler::pages::util::calc_jahres_selektion;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::datum::{Datum, MonatsName};
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct UebersichtEinzelbuchungenViewResult {
    pub liste: Vec<MonatsZusammenfassung>,
    pub selektiertes_jahr: i32,
    pub verfuegbare_jahre: Vec<i32>,
    pub database_version: DatabaseVersion,
}

pub struct UebersichtEinzelbuchungenContext<'a> {
    pub database: &'a Database,
    pub angefordertes_jahr: Option<i32>,
    pub today: Datum,
}

pub struct MonatsZusammenfassung {
    pub monat: MonatsName,
    pub buchungen: Vec<Indiziert<Einzelbuchung>>,
}

pub fn handle_view(
    context: UebersichtEinzelbuchungenContext,
) -> UebersichtEinzelbuchungenViewResult {
    let verfuegbare_jahre: Vec<i32> = context
        .database
        .einzelbuchungen
        .select()
        .extract_unique_values(jahresweise_aggregation)
        .iter()
        .map(|x| x.jahr)
        .collect();

    let selektiertes_jahr = calc_jahres_selektion(
        context.angefordertes_jahr,
        &verfuegbare_jahre,
        context.today,
    );

    let buchungen_des_jahres_selektor = context
        .database
        .einzelbuchungen
        .select()
        .filter(filter_auf_das_jahr(selektiertes_jahr))
        .group_as_list_by(monatsweise_aggregation);

    let mut alle_monate: Vec<MonatsAggregationsIndex> = buchungen_des_jahres_selektor
        .keys()
        .into_iter()
        .map(|x| x.to_owned().clone())
        .collect();
    alle_monate.sort();

    let mut liste = Vec::new();
    for monats_index in alle_monate {
        let monats_buchungen = buchungen_des_jahres_selektor.get(&monats_index).unwrap();
        let monats_zusammenfassung = MonatsZusammenfassung {
            monat: monats_index.format_descriptive_string(),
            buchungen: monats_buchungen.clone(),
        };
        liste.push(monats_zusammenfassung);
    }

    let result = UebersichtEinzelbuchungenViewResult {
        liste,
        selektiertes_jahr,
        verfuegbare_jahre,
        database_version: context.database.db_version.clone(),
    };
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::einzelbuchungen::uebersicht_einzelbuchungen::{
        handle_view, UebersichtEinzelbuchungenContext,
    };
    use crate::model::database::einzelbuchung::builder::demo_einzelbuchung;
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::initial_config::database::generate_initial_database;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_application_state::builder::generate_database_with_einzelbuchungen;

    #[test]
    fn test_handle_view_with_no_datum_angefordert_should_select_dieses_jahr() {
        let database = generate_initial_database();
        let context = UebersichtEinzelbuchungenContext {
            database: &database,
            angefordertes_jahr: None,
            today: Datum::new(1, 1, 2020),
        };
        let result = handle_view(context);

        assert_eq!(result.selektiertes_jahr, 2020);
    }

    #[test]
    fn test_handle_view_with_no_datum_angefordert_should_select_jahr_of_buchung() {
        let database = generate_database_with_einzelbuchungen(vec![demo_einzelbuchung()]);
        let context = UebersichtEinzelbuchungenContext {
            database: &database,
            angefordertes_jahr: None,
            today: Datum::new(1, 1, 2099),
        };
        let result = handle_view(context);

        assert_eq!(result.selektiertes_jahr, demo_einzelbuchung().datum.jahr);
    }

    #[test]
    fn test_handle_view_with_datum_angefordert_should_select_gefordertes_jahr() {
        let database = generate_database_with_einzelbuchungen(vec![demo_einzelbuchung()]);
        let context = UebersichtEinzelbuchungenContext {
            database: &database,
            angefordertes_jahr: Some(2019),
            today: Datum::new(1, 1, 2020),
        };
        let result = handle_view(context);

        assert_eq!(result.selektiertes_jahr, 2019);
    }

    #[test]
    fn test_handle_view_with_einzelbuchungen_should_return_liste() {
        let einzelbuchung = Einzelbuchung {
            datum: Datum::new(1, 1, 2020),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 123, 12),
        };

        let database = generate_database_with_einzelbuchungen(vec![einzelbuchung]);
        let context = UebersichtEinzelbuchungenContext {
            database: &database,
            angefordertes_jahr: None,
            today: Datum::new(1, 1, 2020),
        };
        let result = handle_view(context);

        assert_eq!(result.liste.len(), 1);
        assert_eq!(result.liste[0].monat.monat, "01/2020");
        assert_eq!(result.liste[0].buchungen.len(), 1);

        let result_einzelbuchung = &result.liste[0].buchungen[0];
        assert_eq!(
            result_einzelbuchung.value.datum.to_german_string(),
            "01.01.2020"
        );
        assert_eq!(result_einzelbuchung.value.name.get_name(), "Normal");
        assert_eq!(
            result_einzelbuchung.value.kategorie.get_kategorie(),
            "NeueKategorie"
        );
        assert_eq!(
            result_einzelbuchung.value.betrag.to_german_string(),
            "-123,12"
        );
    }
}
