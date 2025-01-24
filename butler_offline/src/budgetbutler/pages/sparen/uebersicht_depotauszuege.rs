use crate::budgetbutler::database::select::extensions::depotauszug_extension::Depotuebersicht;
use crate::budgetbutler::database::select::functions::filters::filter_auf_das_jahr;
use crate::budgetbutler::database::select::functions::keyextractors::jahresweise_aggregation;
use crate::budgetbutler::pages::util::calc_jahres_selektion;
use crate::model::primitives::datum::Datum;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct UebersichtDepotauszuegeContext<'a> {
    pub database: &'a Database,
    pub angefordertes_jahr: Option<i32>,
    pub today: Datum,
}

pub struct UebersichtDepotauszuegeViewResult {
    pub konten: Vec<Depotuebersicht>,
    pub selektiertes_jahr: i32,
    pub verfuegbare_jahre: Vec<i32>,
    pub database_version: DatabaseVersion,
}

pub fn handle_uebersicht_depotauszuege(
    context: UebersichtDepotauszuegeContext,
) -> UebersichtDepotauszuegeViewResult {
    let verfuegbare_jahre = context
        .database
        .depotauszuege
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
    UebersichtDepotauszuegeViewResult {
        selektiertes_jahr,
        verfuegbare_jahre,
        konten: context
            .database
            .depotauszuege
            .select()
            .filter(filter_auf_das_jahr(selektiertes_jahr))
            .get_kombinierte_depotauszuege(),
        database_version: context.database.db_version.clone(),
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::depotauszug::builder::demo_depotauszug;
    use crate::model::primitives::datum::builder::demo_datum;
    use crate::model::state::persistent_application_state::builder::generate_database_with_depotauszuege;

    #[test]
    fn test_handle_uebersicht_kontos_empty() {
        let database = generate_database_with_depotauszuege(vec![demo_depotauszug()]);
        let context = super::UebersichtDepotauszuegeContext {
            database: &database,
            angefordertes_jahr: Some(demo_depotauszug().datum.jahr),
            today: demo_datum(),
        };

        let result = super::handle_uebersicht_depotauszuege(context);

        assert_eq!(result.konten.len(), 1);
        assert_eq!(
            result.konten[0].konto.konto_name,
            demo_depotauszug().konto.konto_name
        );
        assert_eq!(result.konten[0].datum, demo_depotauszug().datum);
        assert_eq!(result.konten[0].einzelne_werte.len(), 1);
        assert_eq!(
            result.konten[0].einzelne_werte[0].depotwert,
            demo_depotauszug().depotwert
        );
        assert_eq!(
            result.konten[0].einzelne_werte[0].wert,
            demo_depotauszug().wert
        );
    }
}
