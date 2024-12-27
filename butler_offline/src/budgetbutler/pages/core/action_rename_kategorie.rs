use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect};
use crate::budgetbutler::view::routes::CORE_CONFIGURATION;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::persistent_application_state::Database;

pub struct RenameKategorieContext<'a> {
    pub database: &'a Database,
    pub alte_kategorie: Kategorie,
    pub neue_kategorie: Kategorie,
}

pub fn action_rename_kategorie(context: RenameKategorieContext) -> ModificationResult {
    let neue_gemeinsame_buchungen = context
        .database
        .gemeinsame_buchungen
        .change()
        .rename_kategorie(
            context.alte_kategorie.clone(),
            context.neue_kategorie.clone(),
        );

    let neue_einzelbuchungen = context.database.einzelbuchungen.change().rename_kategorie(
        context.alte_kategorie.clone(),
        context.neue_kategorie.clone(),
    );

    let neue_dauerauftraege = context.database.dauerauftraege.change().rename_kategorie(
        context.alte_kategorie.clone(),
        context.neue_kategorie.clone(),
    );

    let neue_datenbank = Database {
        einzelbuchungen: neue_einzelbuchungen,
        dauerauftraege: neue_dauerauftraege,
        db_version: context.database.db_version.clone(),
        gemeinsame_buchungen: neue_gemeinsame_buchungen,
        sparkontos: context.database.sparkontos.clone(),
        sparbuchungen: context.database.sparbuchungen.clone(),
        depotwerte: context.database.depotwerte.clone(),
        order: context.database.order.clone(),
        order_dauerauftraege: context.database.order_dauerauftraege.clone(),
        depotauszuege: context.database.depotauszuege.clone(),
    };

    ModificationResult {
        target: Redirect::to(CORE_CONFIGURATION),
        changed_database: neue_datenbank,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::core::action_rename_kategorie::{
        action_rename_kategorie, RenameKategorieContext,
    };
    use crate::model::database::einzelbuchung::builder::einzelbuchung_with_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::state::persistent_application_state::builder::generate_database_with_einzelbuchungen;

    #[test]
    fn test_action_rename_kategorie() {
        let database = generate_database_with_einzelbuchungen(vec![einzelbuchung_with_kategorie(
            "alte_kategorie",
        )]);

        let result = action_rename_kategorie(RenameKategorieContext {
            neue_kategorie: kategorie("neue_kategorie"),
            alte_kategorie: kategorie("alte_kategorie"),
            database: &database,
        });

        assert_eq!(
            result
                .changed_database
                .einzelbuchungen
                .get(1)
                .value
                .kategorie,
            kategorie("neue_kategorie")
        );
    }
}
