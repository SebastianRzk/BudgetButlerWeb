use crate::budgetbutler::database::sparen::depotwert_beschreibungen::calc_depotwert_beschreibung;
use crate::budgetbutler::view::icons::DELETE;
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_DEPOTAUSZUEGE_UEBERSICHT;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::datum::Datum;
use crate::model::state::non_persistent_application_state::{
    DepotauszugChange, DepotauszugSingleChange,
};
use crate::model::state::persistent_application_state::Database;

pub struct DeleteContext<'a> {
    pub database: &'a Database,
    pub delete_datum: Datum,
    pub delete_konto: KontoReferenz,
}

pub fn delete_depotauszug(context: DeleteContext) -> RedirectResult<DepotauszugChange> {
    let to_delete = context
        .database
        .depotauszuege
        .select()
        .get_konto(context.delete_konto.clone(), context.delete_datum.clone());

    let neue_depotauszuege = context.database.depotauszuege.change().delete_all(
        to_delete
            .iter()
            .map(|depotauszug| depotauszug.index)
            .collect(),
    );

    RedirectResult {
        result: ModificationResult {
            changed_database: context.database.change_depotauszuege(neue_depotauszuege),
            target: Redirect {
                target: SPAREN_DEPOTAUSZUEGE_UEBERSICHT.to_string(),
            },
        },
        change: DepotauszugChange {
            icon: DELETE,
            datum: context.delete_datum,
            konto: context.delete_konto,
            changes: to_delete
                .iter()
                .map(|depotauszug| DepotauszugSingleChange {
                    depotwert_beschreibung: calc_depotwert_beschreibung(
                        &depotauszug.value.depotwert.isin,
                        &context.database,
                    )
                    .description,
                    wert: depotauszug.value.wert.clone(),
                })
                .collect(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::DELETE;
    use crate::model::database::depotauszug::builder::demo_depotauszug_aus_str;
    use crate::model::state::persistent_application_state::builder::generate_database_with_depotauszuege;

    #[test]
    fn test_delete_dauerauftrag() {
        let database = generate_database_with_depotauszuege(vec![demo_depotauszug_aus_str()]);

        let context = super::DeleteContext {
            database: &database,
            delete_datum: demo_depotauszug_aus_str().datum,
            delete_konto: demo_depotauszug_aus_str().konto,
        };

        let result = super::delete_depotauszug(context);

        assert_eq!(
            result
                .result
                .changed_database
                .depotauszuege
                .select()
                .count(),
            0
        );
        assert_eq!(result.change.icon, DELETE);
        assert_eq!(result.change.changes.len(), 1);
        assert_eq!(
            result.change.changes[0].depotwert_beschreibung,
            "Unbekannt (DE000A0D9PT0)"
        );
        assert_eq!(
            result.change.changes[0].wert,
            demo_depotauszug_aus_str().wert
        );
    }
}
