use crate::model::database::depotwert::DepotwertTyp;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::name::Name;
use crate::model::state::non_persistent_application_state::DepotwertChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct AddDepotwertViewResult {
    pub database_version: DatabaseVersion,
    pub bearbeitungsmodus: bool,
    pub action_headline: String,
    pub default_item: DefaultItem,
    pub action_title: String,
    pub letzte_erfassungen: Vec<LetzteErfassung>,
    pub typen: Vec<DepotwertTyp>,
}

pub struct LetzteErfassung {
    pub icon: String,
    pub name: Name,
    pub isin: String,
    pub typ: DepotwertTyp,
}

pub struct AddDepotwertContext<'a> {
    pub database: &'a Database,
    pub depotwerte_changes: &'a Vec<DepotwertChange>,
    pub edit_buchung: Option<u32>,
}

pub struct DefaultItem {
    pub index: u32,
    pub name: Name,
    pub isin: ISIN,
    pub typ: DepotwertTyp,
}

pub fn handle_view(context: AddDepotwertContext) -> AddDepotwertViewResult {
    let mut default_item = DefaultItem {
        index: 0,
        name: Name::empty(),
        typ: DepotwertTyp::ETF,
        isin: ISIN::empty(),
    };
    let mut action_headline = "Depotwert erfassen".to_string();
    let mut action_title = "Depotwert erfassen".to_string();
    let mut bearbeitungsmodus = false;

    if let Some(edit_index) = context.edit_buchung {
        let edit_buchung = context.database.depotwerte.get(edit_index);
        default_item = DefaultItem {
            index: edit_index,
            name: edit_buchung.value.name,
            typ: edit_buchung.value.typ.clone(),
            isin: edit_buchung.value.isin,
        };
        bearbeitungsmodus = true;
        action_headline = "Depotwert bearbeiten".to_string();
        action_title = "Depotwert bearbeiten".to_string();
    }

    AddDepotwertViewResult {
        database_version: context.database.db_version.clone(),
        bearbeitungsmodus,
        action_headline,
        default_item,
        action_title,
        letzte_erfassungen: context
            .depotwerte_changes
            .iter()
            .map(|change| LetzteErfassung {
                icon: change.icon.as_fa.to_string(),
                name: change.name.clone(),
                typ: change.typ.clone(),
                isin: change.isin.isin.clone(),
            })
            .collect(),
        typen: vec![
            DepotwertTyp::ETF,
            DepotwertTyp::Crypto,
            DepotwertTyp::Robot,
            DepotwertTyp::Fond,
            DepotwertTyp::Einzelaktie,
        ],
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::add_depotwert::AddDepotwertContext;
    use crate::budgetbutler::view::icons::PLUS;
    use crate::model::database::depotwert::builder::any_depotwert;
    use crate::model::database::depotwert::DepotwertTyp;
    use crate::model::database::sparkonto::builder::demo_konto;
    use crate::model::primitives::isin::builder::demo_isin;
    use crate::model::primitives::isin::ISIN;
    use crate::model::primitives::name::Name;
    use crate::model::state::non_persistent_application_state::DepotwertChange;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_depotwerte, generate_empty_database,
    };

    #[test]
    pub fn test_handle_view_without_edit_index() {
        let database = generate_database_with_depotwerte(vec![any_depotwert()]);
        let context = AddDepotwertContext {
            database: &database,
            depotwerte_changes: &vec![],
            edit_buchung: None,
        };

        let result = super::handle_view(context);

        assert_eq!(result.database_version.name, "empty");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.action_headline, "Depotwert erfassen");

        assert_eq!(result.default_item.index, 0);
        assert_eq!(result.default_item.name, Name::empty());
        assert_eq!(result.default_item.typ, DepotwertTyp::ETF);
        assert_eq!(result.default_item.isin, ISIN::empty());

        assert_eq!(
            result.typen,
            vec![
                DepotwertTyp::ETF,
                DepotwertTyp::Crypto,
                DepotwertTyp::Robot,
                DepotwertTyp::Fond,
                DepotwertTyp::Einzelaktie,
            ]
        );

        assert_eq!(result.action_title, "Depotwert erfassen");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_with_edit_index() {
        let database = generate_database_with_depotwerte(vec![any_depotwert()]);
        let changes = vec![];
        let context = AddDepotwertContext {
            database: &database,
            edit_buchung: Some(1),
            depotwerte_changes: &changes,
        };

        let result = super::handle_view(context);

        assert_eq!(result.database_version.as_string(), "empty-1-0");
        assert_eq!(result.bearbeitungsmodus, true);
        assert_eq!(result.action_headline, "Depotwert bearbeiten");

        assert_eq!(result.default_item.index, 1);
        assert_eq!(result.default_item.name, any_depotwert().name);
        assert_eq!(result.default_item.typ, any_depotwert().typ);
        assert_eq!(result.default_item.isin, any_depotwert().isin);

        assert_eq!(
            result.typen,
            vec![
                DepotwertTyp::ETF,
                DepotwertTyp::Crypto,
                DepotwertTyp::Robot,
                DepotwertTyp::Fond,
                DepotwertTyp::Einzelaktie,
            ]
        );

        assert_eq!(result.action_title, "Depotwert bearbeiten");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_should_preset_changes() {
        let database = generate_empty_database();
        let changes = vec![DepotwertChange {
            icon: PLUS,
            name: demo_konto().name,
            typ: DepotwertTyp::ETF,
            isin: demo_isin(),
        }];
        let context = AddDepotwertContext {
            database: &database,
            edit_buchung: None,
            depotwerte_changes: &changes,
        };

        let result = super::handle_view(context);

        assert_eq!(result.letzte_erfassungen.len(), 1);
        assert_eq!(result.letzte_erfassungen[0].icon, "fa fa-plus");
        assert_eq!(result.letzte_erfassungen[0].name, demo_konto().name);
        assert_eq!(result.letzte_erfassungen[0].typ, DepotwertTyp::ETF);
        assert_eq!(result.letzte_erfassungen[0].isin, demo_isin().isin);
    }
}
