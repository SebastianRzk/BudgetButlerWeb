use crate::budgetbutler::database::select::functions::filters::filter_auf_depot;
use crate::budgetbutler::database::sparen::depotwert_beschreibungen::calc_depotwert_beschreibungen;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::order::OrderTyp;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::database::sparkonto::Sparkonto;
use crate::model::description::order_typ_description::get_all_order_typ_descriptions;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::name::Name;
use crate::model::primitives::order_betrag::OrderBetrag;
use crate::model::primitives::type_description::TypeDescription;
use crate::model::state::non_persistent_application_state::OrderChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct AddOrderViewResult {
    pub database_version: DatabaseVersion,
    pub bearbeitungsmodus: bool,
    pub action_headline: String,
    pub default_item: DefaultItem,
    pub action_title: String,
    pub letzte_erfassungen: Vec<LetzteErfassung>,
    pub typen: Vec<TypeDescription<OrderTyp>>,
    pub depotwerte: Vec<TypeDescription<String>>,
    pub depots: Vec<Indiziert<Sparkonto>>,
}

pub struct LetzteErfassung {
    pub icon: String,
    pub datum: Datum,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwert: DepotwertReferenz,
    pub wert: OrderBetrag,
}

pub struct AddOrderContext<'a> {
    pub database: &'a Database,
    pub order_changes: &'a Vec<OrderChange>,
    pub edit_buchung: Option<u32>,
    pub heute: Datum,
}

pub struct DefaultItem {
    pub index: u32,
    pub datum: Datum,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwert: DepotwertReferenz,
    pub wert: OrderBetrag,
}

pub fn handle_view(context: AddOrderContext) -> AddOrderViewResult {
    let mut default_item = DefaultItem {
        index: 0,
        name: Name::empty(),
        wert: OrderBetrag::new(BetragOhneVorzeichen::zero(), OrderTyp::Kauf),
        konto: KontoReferenz::new(Name::empty()),
        depotwert: DepotwertReferenz::new(ISIN::empty()),
        datum: context.heute.clone(),
    };
    let mut action_headline = "Order erfassen".to_string();
    let mut action_title = "Order erfassen".to_string();
    let mut bearbeitungsmodus = false;

    if let Some(edit_index) = context.edit_buchung {
        let edit_buchung = context.database.order.get(edit_index);
        default_item = DefaultItem {
            index: edit_index,
            name: edit_buchung.value.name.clone(),
            wert: edit_buchung.value.wert.clone(),
            konto: edit_buchung.value.konto.clone(),
            depotwert: edit_buchung.value.depotwert.clone(),
            datum: edit_buchung.value.datum.clone(),
        };
        bearbeitungsmodus = true;
        action_headline = "Order bearbeiten".to_string();
        action_title = "Order bearbeiten".to_string();
    }

    let result = AddOrderViewResult {
        database_version: context.database.db_version.clone(),
        bearbeitungsmodus,
        action_headline,
        default_item,
        action_title,
        depotwerte: calc_depotwert_beschreibungen(context.database.depotwerte.select().collect()),
        depots: context
            .database
            .sparkontos
            .select()
            .filter(filter_auf_depot)
            .collect(),
        letzte_erfassungen: context
            .order_changes
            .iter()
            .map(|change| LetzteErfassung {
                icon: change.icon.as_fa.to_string(),
                name: change.name.clone(),
                datum: change.datum.clone(),
                konto: change.konto.clone(),
                depotwert: change.depotwert.clone(),
                wert: change.wert.clone(),
            })
            .collect(),
        typen: get_all_order_typ_descriptions(),
    };
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::add_order::AddOrderContext;
    use crate::budgetbutler::view::icons::PLUS;
    use crate::model::database::depotwert::builder::demo_depotwert_referenz;
    use crate::model::database::depotwert::{Depotwert, DepotwertReferenz, DepotwertTyp};
    use crate::model::database::order::builder::any_order;
    use crate::model::database::order::OrderTyp;
    use crate::model::database::sparbuchung::builder::demo_konto_referenz;
    use crate::model::database::sparbuchung::KontoReferenz;
    use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
    use crate::model::primitives::datum::builder::demo_datum;
    use crate::model::primitives::isin::builder::isin;
    use crate::model::primitives::isin::ISIN;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::name::{name, Name};
    use crate::model::primitives::order_betrag::builder::demo_order_betrag;
    use crate::model::state::non_persistent_application_state::OrderChange;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_depotwerte, generate_database_with_orders,
        generate_database_with_sparkontos, generate_empty_database,
    };

    #[test]
    pub fn test_handle_view_without_edit_index() {
        let database = generate_empty_database();
        let context = AddOrderContext {
            database: &database,
            order_changes: &vec![],
            edit_buchung: None,
            heute: demo_datum(),
        };

        let result = super::handle_view(context);

        assert_eq!(result.database_version.name, "empty");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.action_headline, "Order erfassen");

        assert_eq!(result.default_item.index, 0);
        assert_eq!(result.default_item.name, Name::empty());
        assert_eq!(result.default_item.wert.get_typ(), OrderTyp::Kauf);
        assert_eq!(
            result.default_item.wert.get_realer_wert(),
            BetragOhneVorzeichen::zero()
        );
        assert_eq!(result.default_item.konto, KontoReferenz::new(Name::empty()));
        assert_eq!(
            result.default_item.depotwert,
            DepotwertReferenz::new(ISIN::empty())
        );
        assert_eq!(result.default_item.datum, demo_datum());

        assert_eq!(result.action_title, "Order erfassen");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_with_edit_index() {
        let database = generate_database_with_orders(vec![any_order()]);
        let changes = vec![];
        let context = AddOrderContext {
            database: &database,
            edit_buchung: Some(1),
            order_changes: &changes,
            heute: demo_datum(),
        };

        let result = super::handle_view(context);

        assert_eq!(result.database_version.as_string(), "empty-1-0");
        assert_eq!(result.bearbeitungsmodus, true);
        assert_eq!(result.action_headline, "Order bearbeiten");

        assert_eq!(result.default_item.index, 1);
        assert_eq!(result.default_item.name, any_order().name);
        assert_eq!(result.default_item.wert, any_order().wert);
        assert_eq!(result.default_item.konto, any_order().konto);
        assert_eq!(result.default_item.depotwert, any_order().depotwert);
        assert_eq!(result.default_item.datum, any_order().datum);

        assert_eq!(result.action_title, "Order bearbeiten");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_should_preset_changes() {
        let database = generate_empty_database();
        let changes = vec![OrderChange {
            icon: PLUS,
            name: demo_name(),
            datum: demo_datum(),
            konto: demo_konto_referenz(),
            depotwert: demo_depotwert_referenz(),
            wert: demo_order_betrag(),
        }];
        let context = AddOrderContext {
            database: &database,
            edit_buchung: None,
            order_changes: &changes,
            heute: demo_datum(),
        };

        let result = super::handle_view(context);

        assert_eq!(result.letzte_erfassungen.len(), 1);
        assert_eq!(result.letzte_erfassungen[0].icon, "fa fa-plus");
        assert_eq!(result.letzte_erfassungen[0].name, demo_name());
        assert_eq!(result.letzte_erfassungen[0].wert, demo_order_betrag());
        assert_eq!(result.letzte_erfassungen[0].konto, demo_konto_referenz());
        assert_eq!(
            result.letzte_erfassungen[0].depotwert,
            demo_depotwert_referenz()
        );
    }

    #[test]
    fn test_kontos_should_only_contain_depots() {
        let database = generate_database_with_sparkontos(vec![
            Sparkonto {
                kontotyp: Kontotyp::Depot,
                name: name("mein depot"),
            },
            Sparkonto {
                kontotyp: Kontotyp::Sparkonto,
                name: name("mein sparkonto"),
            },
        ]);
        let context = AddOrderContext {
            database: &database,
            edit_buchung: None,
            order_changes: &vec![],
            heute: demo_datum(),
        };

        let result = super::handle_view(context);

        assert_eq!(result.depots.len(), 1);
        assert_eq!(result.depots[0].value.name, name("mein depot"));
    }

    #[test]
    fn test_should_have_described_depotwerte() {
        let database = generate_database_with_depotwerte(vec![Depotwert {
            name: name("demoname"),
            isin: isin("demoisin"),
            typ: DepotwertTyp::ETF,
        }]);

        let context = AddOrderContext {
            database: &database,
            edit_buchung: None,
            order_changes: &vec![],
            heute: demo_datum(),
        };

        let result = super::handle_view(context);

        assert_eq!(result.depotwerte.len(), 1);
        assert_eq!(result.depotwerte[0].value, "demoisin");
        assert_eq!(result.depotwerte[0].description, "demoname (demoisin)");
    }
}
