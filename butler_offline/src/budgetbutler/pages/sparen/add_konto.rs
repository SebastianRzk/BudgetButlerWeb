use crate::model::database::sparkonto::Kontotyp;
use crate::model::primitives::name::Name;
use crate::model::state::non_persistent_application_state::KontoChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct AddKontoViewResult {
    pub database_version: DatabaseVersion,
    pub bearbeitungsmodus: bool,
    pub action_headline: String,
    pub default_item: DefaultItem,
    pub action_title: String,
    pub letzte_erfassungen: Vec<LetzteErfassung>,
    pub kontotypen: Vec<Kontotyp>,
}

pub struct LetzteErfassung {
    pub fa: String,
    pub name: Name,
    pub typ: Kontotyp,
}

pub struct AddKontoContext<'a> {
    pub database: &'a Database,
    pub konto_changes: &'a Vec<KontoChange>,
    pub edit_buchung: Option<u32>,
}

pub struct DefaultItem {
    pub index: u32,
    pub name: Name,
    pub typ: Kontotyp,
}

pub fn handle_view(context: AddKontoContext) -> AddKontoViewResult {
    let mut default_item = DefaultItem {
        index: 0,
        name: Name::empty(),
        typ: Kontotyp::Depot,
    };
    let mut action_headline = "Konto erfassen".to_string();
    let mut action_title = "Konto erfassen".to_string();
    let mut bearbeitungsmodus = false;

    if let Some(edit_index) = context.edit_buchung {
        let edit_buchung = context.database.sparkontos.get(edit_index);
        default_item = DefaultItem {
            index: edit_index,
            name: edit_buchung.value.name,
            typ: edit_buchung.value.kontotyp,
        };
        bearbeitungsmodus = true;
        action_headline = "Konto bearbeiten".to_string();
        action_title = "Konto bearbeiten".to_string();
    }

    let result = AddKontoViewResult {
        database_version: context.database.db_version.clone(),
        bearbeitungsmodus,
        action_headline,
        default_item,
        kontotypen: vec![
            Kontotyp::Depot,
            Kontotyp::GenossenschaftsAnteile,
            Kontotyp::Sparkonto,
        ],
        action_title,
        letzte_erfassungen: context
            .konto_changes
            .iter()
            .map(|change| LetzteErfassung {
                fa: change.icon.clone(),
                name: change.name.clone(),
                typ: change.typ.clone(),
            })
            .collect(),
    };
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::add_konto::AddKontoContext;
    use crate::model::database::sparkonto::builder::demo_konto;
    use crate::model::database::sparkonto::Kontotyp;
    use crate::model::primitives::name::Name;
    use crate::model::state::non_persistent_application_state::KontoChange;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_sparkontos, generate_empty_database,
    };

    #[test]
    pub fn test_handle_view_without_edit_index() {
        let database = generate_database_with_sparkontos(vec![demo_konto()]);
        let context = AddKontoContext {
            database: &database,
            konto_changes: &vec![],
            edit_buchung: None,
        };

        let result = super::handle_view(context);

        assert_eq!(result.database_version.name, "empty");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.action_headline, "Konto erfassen");

        assert_eq!(result.default_item.index, 0);
        assert_eq!(result.default_item.name, Name::empty());
        assert_eq!(result.default_item.typ, Kontotyp::Depot);

        assert_eq!(
            result.kontotypen,
            vec![
                Kontotyp::Depot,
                Kontotyp::GenossenschaftsAnteile,
                Kontotyp::Sparkonto
            ]
        );
        assert_eq!(result.action_title, "Konto erfassen");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_with_edit_index() {
        let database = generate_database_with_sparkontos(vec![demo_konto()]);
        let changes = vec![];
        let context = AddKontoContext {
            database: &database,
            edit_buchung: Some(1),
            konto_changes: &changes,
        };

        let result = super::handle_view(context);

        assert_eq!(result.database_version.as_string(), "empty-1-0");
        assert_eq!(result.bearbeitungsmodus, true);
        assert_eq!(result.action_headline, "Konto bearbeiten");

        assert_eq!(result.default_item.index, 1);
        assert_eq!(result.default_item.name, demo_konto().name);
        assert_eq!(result.default_item.typ, demo_konto().kontotyp);

        assert_eq!(
            result.kontotypen,
            vec![
                Kontotyp::Depot,
                Kontotyp::GenossenschaftsAnteile,
                Kontotyp::Sparkonto
            ]
        );
        assert_eq!(result.action_title, "Konto bearbeiten");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_should_preset_changes() {
        let database = generate_empty_database();
        let changes = vec![KontoChange {
            icon: "fa fa-plus".to_string(),
            name: demo_konto().name,
            typ: demo_konto().kontotyp,
        }];
        let context = AddKontoContext {
            database: &database,
            edit_buchung: None,
            konto_changes: &changes,
        };

        let result = super::handle_view(context);

        assert_eq!(result.letzte_erfassungen.len(), 1);
        assert_eq!(result.letzte_erfassungen[0].fa, "fa fa-plus");
        assert_eq!(result.letzte_erfassungen[0].name, demo_konto().name);
        assert_eq!(result.letzte_erfassungen[0].typ, demo_konto().kontotyp);
    }
}
