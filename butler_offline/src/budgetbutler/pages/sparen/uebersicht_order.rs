use crate::budgetbutler::database::select::functions::datatypes::MonatsAggregationsIndex;
use crate::budgetbutler::database::select::functions::filters::filter_auf_das_jahr;
use crate::budgetbutler::database::select::functions::keyextractors::{
    jahresweise_aggregation, monatsweise_aggregation,
};
use crate::budgetbutler::database::sparen::depotwert_beschreibungen::calc_depotwert_beschreibung;
use crate::budgetbutler::pages::util::calc_jahres_selektion;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::datum::{Datum, MonatsName};
use crate::model::primitives::name::Name;
use crate::model::primitives::order_betrag::OrderBetrag;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct UebersichtOrderViewResult {
    pub liste: Vec<MonatsZusammenfassung>,
    pub selektiertes_jahr: i32,
    pub verfuegbare_jahre: Vec<i32>,
    pub database_version: DatabaseVersion,
}

pub struct UebersichtOrderContext<'a> {
    pub database: &'a Database,
    pub angefordertes_jahr: Option<i32>,
    pub today: Datum,
}

pub struct MonatsZusammenfassung {
    pub monat: MonatsName,
    pub buchungen: Vec<BeschriebeneOrder>,
}

pub struct BeschriebeneOrder {
    pub index: u32,
    pub datum: Datum,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwertbeschreibung: String,
    pub wert: OrderBetrag,
    pub dynamisch: bool,
}

pub fn handle_view(context: UebersichtOrderContext) -> UebersichtOrderViewResult {
    let verfuegbare_jahre: Vec<i32> = context
        .database
        .order
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
        .order
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
            buchungen: monats_buchungen
                .iter()
                .map(|x| BeschriebeneOrder {
                    index: x.index,
                    datum: x.value.datum.clone(),
                    name: x.value.name.clone(),
                    konto: x.value.konto.clone(),
                    depotwertbeschreibung: calc_depotwert_beschreibung(
                        &x.value.depotwert.isin,
                        context.database,
                    )
                    .description,
                    wert: x.value.wert.clone(),
                    dynamisch: x.dynamisch,
                })
                .collect(),
        };
        liste.push(monats_zusammenfassung);
    }

    let result = UebersichtOrderViewResult {
        liste,
        selektiertes_jahr,
        verfuegbare_jahre,
        database_version: context.database.db_version.clone(),
    };
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_order::UebersichtOrderContext;
    use crate::model::database::depotwert::builder::depotwert_referenz;
    use crate::model::database::order::builder::any_order;
    use crate::model::database::order::Order;
    use crate::model::database::order::OrderTyp::Kauf;
    use crate::model::database::sparbuchung::builder::demo_konto_referenz;
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::name;
    use crate::model::primitives::order_betrag::OrderBetrag;
    use crate::model::state::persistent_application_state::builder::generate_database_with_orders;

    #[test]
    fn test_handle_view_with_no_datum_angefordert_should_select_dieses_jahr() {
        let database = generate_database_with_orders(vec![any_order()]);
        let context = UebersichtOrderContext {
            database: &database,
            angefordertes_jahr: None,
            today: Datum::new(1, 1, 2020),
        };
        let result = super::handle_view(context);

        assert_eq!(result.selektiertes_jahr, 2020);
    }

    #[test]
    fn test_handle_view_with_datum_angefordert_should_select_gefordertes_jahr() {
        let database = generate_database_with_orders(vec![any_order()]);
        let context = UebersichtOrderContext {
            database: &database,
            angefordertes_jahr: Some(2019),
            today: Datum::new(1, 1, 2020),
        };
        let result = super::handle_view(context);

        assert_eq!(result.selektiertes_jahr, 2019);
    }

    #[test]
    fn test_handle_view_with_einzelbuchungen_should_return_liste() {
        let order = Order {
            datum: Datum::new(1, 1, 2020),
            name: name("Normal"),
            wert: OrderBetrag::new(BetragOhneVorzeichen::new(123, 12), Kauf),
            konto: demo_konto_referenz(),
            depotwert: depotwert_referenz("demo isin"),
        };

        let database = generate_database_with_orders(vec![order]);
        let context = UebersichtOrderContext {
            database: &database,
            angefordertes_jahr: None,
            today: Datum::new(1, 1, 2020),
        };
        let result = super::handle_view(context);

        assert_eq!(result.liste.len(), 1);
        assert_eq!(result.liste[0].monat.monat, "01/2020");
        assert_eq!(result.liste[0].buchungen.len(), 1);

        let result_einzelbuchung = &result.liste[0].buchungen[0];
        assert_eq!(result_einzelbuchung.datum.to_german_string(), "01.01.2020");
        assert_eq!(result_einzelbuchung.name.get_name(), "Normal");
        assert_eq!(result_einzelbuchung.konto, demo_konto_referenz());
        assert_eq!(
            result_einzelbuchung
                .wert
                .get_realer_wert()
                .to_german_string(),
            "123,12"
        );
    }
}
