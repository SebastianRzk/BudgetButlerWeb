use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::indiziert::Indiziert;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct UebersichtGemeinsameBuchungenViewResult {
    pub liste: Vec<Indiziert<GemeinsameBuchung>>,
    pub database_version: DatabaseVersion,
}

pub struct UebersichtGemeinsameBuchungenContext<'a> {
    pub database: &'a Database,
}

pub fn handle_view(
    context: UebersichtGemeinsameBuchungenContext,
) -> UebersichtGemeinsameBuchungenViewResult {
    let result = UebersichtGemeinsameBuchungenViewResult {
        liste: context.database.gemeinsame_buchungen.select().collect(),
        database_version: context.database.db_version.clone(),
    };
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::gemeinsame_buchungen::uebersicht_gemeinsame_buchungen::{
        handle_view, UebersichtGemeinsameBuchungenContext,
    };
    use crate::model::database::gemeinsame_buchung::builder::demo_gemeinsame_buchung;
    use crate::model::state::persistent_application_state::builder::generate_database_with_gemeinsamen_buchungen;

    #[test]
    fn test_handle_view() {
        let database =
            generate_database_with_gemeinsamen_buchungen(vec![demo_gemeinsame_buchung()]);
        let context = UebersichtGemeinsameBuchungenContext {
            database: &database,
        };

        let result = handle_view(context);

        assert_eq!(result.liste.len(), 1);
        assert_eq!(result.liste[0].value, demo_gemeinsame_buchung());
    }
}
