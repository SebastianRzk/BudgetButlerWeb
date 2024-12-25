use crate::budgetbutler::database::sparen::depotwert_beschreibungen::calc_depotwert_beschreibung;
use crate::budgetbutler::view::icons::{PENCIL, PLUS};
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_DEPOTAUSZUG_ADD;
use crate::model::database::depotauszug::Depotauszug;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::state::non_persistent_application_state::{
    DepotauszugChange, DepotauszugSingleChange,
};
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::depotauszuege::Depotauszuege;

pub struct SubmitDepotauszugContext<'a> {
    pub database: &'a Database,
    pub mode: Mode,
    pub datum: Datum,
    pub konto: KontoReferenz,
    pub auszuege: Vec<Auszug>,
}

#[derive(Clone, PartialEq, Eq, Debug)]
pub enum Mode {
    Add,
    Edit,
}

#[derive(Clone, PartialEq, Eq, Debug)]
pub struct Auszug {
    pub depotwert_referenz: DepotwertReferenz,
    pub wert: Betrag,
}

pub fn submit_depotauszug(context: SubmitDepotauszugContext) -> RedirectResult<DepotauszugChange> {
    let neue_depotauszuege: Depotauszuege;
    let change: DepotauszugChange;

    if context.mode == Mode::Add {
        let depotauszuege = context
            .auszuege
            .iter()
            .map(|auszug| Depotauszug {
                datum: context.datum.clone(),
                konto: context.konto.clone(),
                depotwert: auszug.depotwert_referenz.clone(),
                wert: auszug.wert.clone(),
            })
            .collect();
        neue_depotauszuege = context
            .database
            .depotauszuege
            .change()
            .insert_all(depotauszuege);
        change = DepotauszugChange {
            konto: context.konto.clone(),
            datum: context.datum.clone(),
            icon: PLUS,
            changes: context
                .auszuege
                .iter()
                .map(|auszug| DepotauszugSingleChange {
                    depotwert_beschreibung: calc_depotwert_beschreibung(
                        &auszug.depotwert_referenz.isin,
                        context.database,
                    )
                    .description,
                    wert: auszug.wert.clone(),
                })
                .collect(),
        }
    } else {
        let depotauszuege: Vec<Depotauszug> = context
            .auszuege
            .iter()
            .map(|auszug| Depotauszug {
                datum: context.datum.clone(),
                konto: context.konto.clone(),
                depotwert: auszug.depotwert_referenz.clone(),
                wert: auszug.wert.clone(),
            })
            .collect();
        let mut c = context.database.depotauszuege.clone();
        for auszug in depotauszuege {
            c = c.change().update_auszug(auszug);
        }
        neue_depotauszuege = c;

        change = DepotauszugChange {
            konto: context.konto.clone(),
            datum: context.datum.clone(),
            icon: PENCIL,
            changes: context
                .auszuege
                .iter()
                .map(|auszug| DepotauszugSingleChange {
                    depotwert_beschreibung: calc_depotwert_beschreibung(
                        &auszug.depotwert_referenz.isin,
                        context.database,
                    )
                    .description,
                    wert: auszug.wert.clone(),
                })
                .collect(),
        }
    }

    let new_database = context.database.change_depotauszuege(neue_depotauszuege);

    RedirectResult {
        result: ModificationResult {
            changed_database: new_database,
            target: Redirect {
                target: SPAREN_DEPOTAUSZUG_ADD.to_string(),
            },
        },
        change,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::action_add_edit_depotauszug::{
        Auszug, Mode, SubmitDepotauszugContext,
    };
    use crate::model::database::depotauszug::Depotauszug;
    use crate::model::database::depotwert::builder::demo_depotwert_referenz;
    use crate::model::database::sparbuchung::builder::demo_konto_referenz;
    use crate::model::primitives::betrag::builder::vier;
    use crate::model::primitives::datum::builder::demo_datum;
    use crate::model::state::persistent_application_state::builder::generate_empty_database;

    #[test]
    fn test_add_depotauszug() {
        let database = generate_empty_database();
        let context = SubmitDepotauszugContext {
            database: &database,
            datum: demo_datum(),
            konto: demo_konto_referenz(),
            mode: Mode::Add,
            auszuege: vec![Auszug {
                depotwert_referenz: demo_depotwert_referenz(),
                wert: vier(),
            }],
        };

        let result = super::submit_depotauszug(context);

        assert_eq!(
            result
                .result
                .changed_database
                .depotauszuege
                .depotauszuege
                .len(),
            1
        );
        assert_eq!(
            result
                .result
                .changed_database
                .depotauszuege
                .select()
                .first()
                .value,
            Depotauszug {
                datum: demo_datum(),
                konto: demo_konto_referenz(),
                depotwert: demo_depotwert_referenz(),
                wert: vier(),
            }
        );
        assert_eq!(result.change.changes.len(), 1);
        assert_eq!(
            result.change.changes[0].depotwert_beschreibung,
            "Unbekannt (TestISIN)"
        );
        assert_eq!(result.change.changes[0].wert, vier());
    }
}
