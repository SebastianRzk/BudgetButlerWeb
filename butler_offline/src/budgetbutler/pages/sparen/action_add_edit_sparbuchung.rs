use crate::budgetbutler::view::icons::{Icon, PENCIL, PLUS};
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_SPARBUCHUNG_ADD;
use crate::model::database::sparbuchung::{KontoReferenz, Sparbuchung, SparbuchungTyp};
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::name::Name;
use crate::model::state::non_persistent_application_state::SparbuchungChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::sparbuchungen::Sparbuchungen;

pub struct SubmitSparbuchungContext<'a> {
    pub database: &'a Database,
    pub edit_index: Option<u32>,
    pub datum: Datum,
    pub name: Name,
    pub wert: BetragOhneVorzeichen,
    pub typ: SparbuchungTyp,
    pub konto: KontoReferenz,
}

pub fn submit_sparbuchung(context: SubmitSparbuchungContext) -> RedirectResult<SparbuchungChange> {
    let buchung = Sparbuchung {
        name: context.name.clone(),
        datum: context.datum.clone(),
        wert: context.wert.clone(),
        typ: context.typ.clone(),
        konto: context.konto.clone(),
    };
    let neue_sparbuchungen: Sparbuchungen;
    let icon: Icon;

    if let Some(index) = context.edit_index {
        icon = PENCIL;
        neue_sparbuchungen = context
            .database
            .sparbuchungen
            .change()
            .edit(index, buchung.clone())
    } else {
        icon = PLUS;
        neue_sparbuchungen = context
            .database
            .sparbuchungen
            .change()
            .insert(buchung.clone())
    }

    let new_database = context.database.change_sparbuchungen(neue_sparbuchungen);

    RedirectResult {
        result: ModificationResult {
            changed_database: new_database,
            target: Redirect {
                target: SPAREN_SPARBUCHUNG_ADD.to_string(),
            },
        },
        change: SparbuchungChange {
            icon,
            name: buchung.name.clone(),
            datum: buchung.datum.clone(),
            wert: buchung.wert.clone(),
            typ: buchung.typ.clone(),
            konto: buchung.konto.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::action_add_edit_sparbuchung::{
        submit_sparbuchung, SubmitSparbuchungContext,
    };
    use crate::budgetbutler::view::icons::PLUS;
    use crate::model::database::sparbuchung::builder::demo_konto_referenz;
    use crate::model::database::sparbuchung::{Sparbuchung, SparbuchungTyp};
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::state::persistent_application_state::builder::generate_empty_database;

    #[test]
    fn test_submit_sparbuchung() {
        let database = generate_empty_database();

        let result = submit_sparbuchung(SubmitSparbuchungContext {
            database: &database,
            edit_index: None,
            name: demo_name(),
            datum: Datum::new(1, 2, 2021),
            wert: u_zwei(),
            typ: SparbuchungTyp::ManuelleEinzahlung,
            konto: demo_konto_referenz(),
        });

        assert_eq!(
            result
                .result
                .changed_database
                .sparbuchungen
                .select()
                .count(),
            1
        );
        assert_eq!(
            result.result.changed_database.sparbuchungen.get(0).value,
            Sparbuchung {
                name: demo_name(),
                datum: Datum::new(1, 2, 2021),
                wert: u_zwei(),
                typ: SparbuchungTyp::ManuelleEinzahlung,
                konto: demo_konto_referenz(),
            }
        );

        assert_eq!(result.change.icon, PLUS);
        assert_eq!(result.change.name, demo_name());
        assert_eq!(result.change.datum, Datum::new(1, 2, 2021));
        assert_eq!(result.change.wert, u_zwei());
        assert_eq!(result.change.typ, SparbuchungTyp::ManuelleEinzahlung);
    }
}
