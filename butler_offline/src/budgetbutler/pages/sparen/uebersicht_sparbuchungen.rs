use crate::budgetbutler::database::select::functions::datatypes::MonatsAggregationsIndex;
use crate::budgetbutler::database::select::functions::filters::filter_auf_das_jahr;
use crate::budgetbutler::database::select::functions::keyextractors::{
    jahresweise_aggregation, monatsweise_aggregation,
};
use crate::budgetbutler::pages::util::calc_jahres_selektion;
use crate::model::database::sparbuchung::Sparbuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::datum::{Datum, MonatsName};
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct UebersichtSparbuchungenViewResult {
    pub liste: Vec<MonatsZusammenfassung>,
    pub selektiertes_jahr: i32,
    pub verfuegbare_jahre: Vec<i32>,
    pub database_version: DatabaseVersion,
}

pub struct UebersichtSparbuchungenContext<'a> {
    pub database: &'a Database,
    pub angefordertes_jahr: Option<i32>,
    pub today: Datum,
}

pub struct MonatsZusammenfassung {
    pub monat: MonatsName,
    pub buchungen: Vec<Indiziert<Sparbuchung>>,
}

pub fn handle_view(context: UebersichtSparbuchungenContext) -> UebersichtSparbuchungenViewResult {
    let verfuegbare_jahre = context
        .database
        .sparbuchungen
        .select()
        .extract_unique_values(jahresweise_aggregation)
        .iter()
        .map(|x| x.jahr)
        .collect();

    let selektiertes_jahr = calc_jahres_selektion(
        context.angefordertes_jahr,
        &verfuegbare_jahre,
        context.today.clone(),
    );

    let buchungen_des_jahres_selektor = context
        .database
        .sparbuchungen
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

    let result = UebersichtSparbuchungenViewResult {
        liste,
        selektiertes_jahr,
        verfuegbare_jahre,
        database_version: context.database.db_version.clone(),
    };
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_sparbuchungen::UebersichtSparbuchungenContext;
    use crate::model::database::sparbuchung::builder::{any_sparbuchung, demo_konto_referenz};
    use crate::model::database::sparbuchung::{Sparbuchung, SparbuchungTyp};
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_application_state::builder::generate_database_with_sparbuchungen;

    #[test]
    fn test_handle_view_with_no_datum_angefordert_should_select_dieses_jahr() {
        let database = generate_database_with_sparbuchungen(vec![any_sparbuchung()]);
        let context = UebersichtSparbuchungenContext {
            database: &database,
            angefordertes_jahr: None,
            today: Datum::new(1, 1, 2020),
        };
        let result = super::handle_view(context);

        assert_eq!(result.selektiertes_jahr, 2020);
    }

    #[test]
    fn test_handle_view_with_datum_angefordert_should_select_gefordertes_jahr() {
        let database = generate_database_with_sparbuchungen(vec![any_sparbuchung()]);
        let context = UebersichtSparbuchungenContext {
            database: &database,
            angefordertes_jahr: Some(2019),
            today: Datum::new(1, 1, 2020),
        };
        let result = super::handle_view(context);

        assert_eq!(result.selektiertes_jahr, 2019);
    }

    #[test]
    fn test_handle_view_with_sparbuchung_should_return_liste() {
        let sparbuchung = Sparbuchung {
            datum: Datum::new(1, 1, 2020),
            name: name("Normal"),
            wert: BetragOhneVorzeichen::new(123, 12),
            konto: demo_konto_referenz(),
            typ: SparbuchungTyp::SonstigeKosten,
        };

        let database = generate_database_with_sparbuchungen(vec![sparbuchung]);
        let context = UebersichtSparbuchungenContext {
            database: &database,
            angefordertes_jahr: None,
            today: Datum::new(1, 1, 2020),
        };
        let result = super::handle_view(context);

        assert_eq!(result.liste.len(), 1);
        assert_eq!(result.liste[0].monat.monat, "01/2020");
        assert_eq!(result.liste[0].buchungen.len(), 1);

        let result_einzelbuchung = &result.liste[0].buchungen[0];
        assert_eq!(
            result_einzelbuchung.value.datum.to_german_string(),
            "01.01.2020"
        );
        assert_eq!(result_einzelbuchung.value.name.get_name(), "Normal");
        assert_eq!(result_einzelbuchung.value.konto, demo_konto_referenz());
        assert_eq!(result_einzelbuchung.value.wert.to_german_string(), "123,12");
    }
}
