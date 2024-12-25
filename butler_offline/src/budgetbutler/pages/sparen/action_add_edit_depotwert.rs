use crate::budgetbutler::view::icons::{Icon, PENCIL, PLUS};
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_DEPOTWERT_ADD;
use crate::model::database::depotwert::{Depotwert, DepotwertTyp};
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::name::Name;
use crate::model::state::non_persistent_application_state::DepotwertChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::depotwerte::Depotwerte;

pub struct SubmitDepotwertContext<'a> {
    pub database: &'a Database,
    pub edit_index: Option<u32>,
    pub name: Name,
    pub typ: DepotwertTyp,
    pub isin: ISIN,
}

pub fn submit_depotwert(context: SubmitDepotwertContext) -> RedirectResult<DepotwertChange> {
    let depotwert = Depotwert {
        name: context.name.clone(),
        typ: context.typ.clone(),
        isin: context.isin.clone(),
    };
    let neue_depotwerte: Depotwerte;
    let icon: Icon;

    if let Some(index) = context.edit_index {
        icon = PENCIL;
        neue_depotwerte = context
            .database
            .depotwerte
            .change()
            .edit(index, depotwert.clone())
    } else {
        icon = PLUS;
        neue_depotwerte = context
            .database
            .depotwerte
            .change()
            .insert(depotwert.clone())
    }

    let new_database = context.database.change_depotwerte(neue_depotwerte);

    RedirectResult {
        result: ModificationResult {
            changed_database: new_database,
            target: Redirect {
                target: SPAREN_DEPOTWERT_ADD.to_string(),
            },
        },
        change: DepotwertChange {
            icon,
            name: depotwert.name.clone(),
            typ: depotwert.typ.clone(),
            isin: depotwert.isin.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::action_add_edit_depotwert::SubmitDepotwertContext;
    use crate::budgetbutler::view::icons::PLUS;
    use crate::model::database::depotwert::{Depotwert, DepotwertTyp};
    use crate::model::primitives::isin::builder::isin;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::state::persistent_application_state::builder::generate_empty_database;

    #[test]
    fn test_submit_depotwert() {
        let database = generate_empty_database();

        let result = super::submit_depotwert(SubmitDepotwertContext {
            database: &database,
            edit_index: None,
            name: demo_name(),
            typ: DepotwertTyp::Einzelaktie,
            isin: isin("DE000A0WMPJ6"),
        });

        assert_eq!(
            result.result.changed_database.depotwerte.select().count(),
            1
        );
        assert_eq!(
            result.result.changed_database.depotwerte.get(0).value,
            Depotwert {
                name: demo_name(),
                isin: isin("DE000A0WMPJ6"),
                typ: DepotwertTyp::Einzelaktie,
            }
        );

        assert_eq!(result.change.icon, PLUS);
        assert_eq!(result.change.name, demo_name());
        assert_eq!(result.change.typ, DepotwertTyp::Einzelaktie);
        assert_eq!(result.change.isin, isin("DE000A0WMPJ6"));
    }
}
