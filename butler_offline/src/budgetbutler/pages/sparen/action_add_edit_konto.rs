use crate::budgetbutler::view::icons::{Icon, PENCIL, PLUS};
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_SPARKONTO_ADD;
use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
use crate::model::primitives::name::Name;
use crate::model::state::non_persistent_application_state::KontoChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::sparkontos::Sparkontos;

pub struct SubmitKontoContext<'a> {
    pub database: &'a Database,
    pub edit_index: Option<u32>,
    pub name: Name,
    pub kontotyp: Kontotyp,
}

pub fn submit_sparkonto(context: SubmitKontoContext) -> RedirectResult<KontoChange> {
    let buchung = Sparkonto {
        name: context.name.clone(),
        kontotyp: context.kontotyp.clone(),
    };
    let neue_sparkontos: Sparkontos;
    let icon: Icon;

    if let Some(index) = context.edit_index {
        icon = PENCIL;
        neue_sparkontos = context
            .database
            .sparkontos
            .change()
            .edit(index, buchung.clone())
    } else {
        icon = PLUS;
        neue_sparkontos = context.database.sparkontos.change().insert(buchung.clone())
    }

    let new_database = context.database.change_sparkontos(neue_sparkontos);

    RedirectResult {
        result: ModificationResult {
            changed_database: new_database,
            target: Redirect {
                target: SPAREN_SPARKONTO_ADD.to_string(),
            },
        },
        change: KontoChange {
            icon: icon.as_fa.to_string(),
            name: buchung.name.clone(),
            typ: buchung.kontotyp.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::action_add_edit_konto::{
        submit_sparkonto, SubmitKontoContext,
    };
    use crate::budgetbutler::view::icons::PLUS;
    use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::state::persistent_application_state::builder::generate_empty_database;

    #[test]
    fn test_submit_sparkonto() {
        let database = generate_empty_database();

        let result = submit_sparkonto(SubmitKontoContext {
            database: &database,
            edit_index: None,
            name: demo_name(),
            kontotyp: Kontotyp::Sparkonto,
        });

        assert_eq!(
            result.result.changed_database.sparkontos.select().count(),
            1
        );
        assert_eq!(
            result.result.changed_database.sparkontos.get(0).value,
            Sparkonto {
                name: demo_name(),
                kontotyp: Kontotyp::Sparkonto,
            }
        );

        assert_eq!(result.change.icon, PLUS.as_fa.to_string());
        assert_eq!(result.change.name, demo_name());
        assert_eq!(result.change.typ, Kontotyp::Sparkonto);
    }
}
