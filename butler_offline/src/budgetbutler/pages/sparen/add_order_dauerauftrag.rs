use crate::budgetbutler::database::sparen::depotwert_beschreibungen::calc_depotwert_beschreibungen;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::order::OrderTyp;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
use crate::model::description::order_typ_description::get_all_order_typ_descriptions;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::name::Name;
use crate::model::primitives::order_betrag::OrderBetrag;
use crate::model::primitives::rhythmus::Rhythmus;
use crate::model::primitives::type_description::TypeDescription;
use crate::model::state::non_persistent_application_state::OrderDauerauftragChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct AddOrderDauerauftragViewResult {
    pub database_version: DatabaseVersion,
    pub bearbeitungsmodus: bool,
    pub action_headline: String,
    pub default_item: DefaultItem,
    pub action_title: String,
    pub letzte_erfassungen: Vec<LetzteErfassung>,
    pub typen: Vec<TypeDescription<OrderTyp>>,
    pub depotwerte: Vec<TypeDescription<String>>,
    pub depots: Vec<Indiziert<Sparkonto>>,
    pub rhythmen: Vec<Rhythmus>,
}

pub struct LetzteErfassung {
    pub icon: String,
    pub start_datum: Datum,
    pub ende_datum: Datum,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwert: DepotwertReferenz,
    pub wert: OrderBetrag,
    pub rhythmus: Rhythmus,
}

pub struct AddOrderDauerauftragContext<'a> {
    pub database: &'a Database,
    pub order_dauerauftrag_changes: &'a Vec<OrderDauerauftragChange>,
    pub edit_buchung: Option<u32>,
    pub heute: Datum,
}

pub struct DefaultItem {
    pub index: u32,
    pub start_datum: Datum,
    pub ende_datum: Datum,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwert: DepotwertReferenz,
    pub wert: OrderBetrag,
    pub rhythmus: Rhythmus,
}

pub fn handle_view(context: AddOrderDauerauftragContext) -> AddOrderDauerauftragViewResult {
    let mut default_item = DefaultItem {
        index: 0,
        name: Name::empty(),
        wert: OrderBetrag::new(BetragOhneVorzeichen::zero(), OrderTyp::Kauf),
        konto: KontoReferenz::new(Name::empty()),
        depotwert: DepotwertReferenz::new(ISIN::empty()),
        start_datum: context.heute.clone(),
        ende_datum: context.heute.clone(),
        rhythmus: Rhythmus::Monatlich,
    };
    let mut action_headline = "Order-Dauerauftrag erfassen".to_string();
    let mut action_title = "Order-Dauerauftrag erfassen".to_string();
    let mut bearbeitungsmodus = false;

    if let Some(edit_index) = context.edit_buchung {
        let edit_buchung = context.database.order_dauerauftraege.get(edit_index);
        default_item = DefaultItem {
            index: edit_index,
            name: edit_buchung.value.name.clone(),
            wert: edit_buchung.value.wert.clone(),
            konto: edit_buchung.value.konto.clone(),
            depotwert: edit_buchung.value.depotwert.clone(),
            start_datum: edit_buchung.value.start_datum.clone(),
            ende_datum: edit_buchung.value.ende_datum.clone(),
            rhythmus: edit_buchung.value.rhythmus.clone(),
        };
        bearbeitungsmodus = true;
        action_headline = "Order-Dauerauftrag bearbeiten".to_string();
        action_title = "Order-Dauerauftrag bearbeiten".to_string();
    }

    let result = AddOrderDauerauftragViewResult {
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
            .filter(|sparkonto| sparkonto.value.kontotyp == Kontotyp::Depot)
            .collect(),
        letzte_erfassungen: context
            .order_dauerauftrag_changes
            .iter()
            .map(|change| LetzteErfassung {
                icon: change.icon.as_fa.to_string(),
                name: change.name.clone(),
                konto: change.konto.clone(),
                depotwert: change.depotwert.clone(),
                wert: change.wert.clone(),
                start_datum: change.start_datum.clone(),
                ende_datum: change.ende_datum.clone(),
                rhythmus: change.rhythmus.clone(),
            })
            .collect(),
        typen: get_all_order_typ_descriptions(),
        rhythmen: vec![
            Rhythmus::Monatlich,
            Rhythmus::Vierteljaehrlich,
            Rhythmus::Halbjaehrlich,
            Rhythmus::Jaehrlich,
        ],
    };
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::add_order_dauerauftrag::AddOrderDauerauftragContext;
    use crate::budgetbutler::view::icons::PLUS;
    use crate::model::database::depotwert::builder::demo_depotwert_referenz;
    use crate::model::database::depotwert::{Depotwert, DepotwertReferenz, DepotwertTyp};
    use crate::model::database::order::OrderTyp;
    use crate::model::database::order_dauerauftrag::builder::any_order_dauerauftrag;
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
    use crate::model::primitives::rhythmus::Rhythmus;
    use crate::model::state::non_persistent_application_state::OrderDauerauftragChange;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_depotwerte, generate_database_with_order_dauerauftraege,
        generate_database_with_sparkontos, generate_empty_database,
    };

    #[test]
    pub fn test_handle_view_without_edit_index() {
        let database = generate_empty_database();
        let context = AddOrderDauerauftragContext {
            database: &database,
            order_dauerauftrag_changes: &vec![],
            edit_buchung: None,
            heute: demo_datum(),
        };

        let result = super::handle_view(context);

        assert_eq!(result.database_version.name, "empty");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.action_headline, "Order-Dauerauftrag erfassen");

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
        assert_eq!(result.default_item.start_datum, demo_datum());
        assert_eq!(result.default_item.ende_datum, demo_datum());
        assert_eq!(result.default_item.rhythmus, Rhythmus::Monatlich);

        assert_eq!(result.action_title, "Order-Dauerauftrag erfassen");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_with_edit_index() {
        let database = generate_database_with_order_dauerauftraege(vec![any_order_dauerauftrag()]);
        let changes = vec![];
        let context = AddOrderDauerauftragContext {
            database: &database,
            edit_buchung: Some(1),
            order_dauerauftrag_changes: &changes,
            heute: demo_datum(),
        };

        let result = super::handle_view(context);

        assert_eq!(result.database_version.as_string(), "empty-1-0");
        assert_eq!(result.bearbeitungsmodus, true);
        assert_eq!(result.action_headline, "Order-Dauerauftrag bearbeiten");

        assert_eq!(result.default_item.index, 1);
        assert_eq!(result.default_item.name, any_order_dauerauftrag().name);
        assert_eq!(result.default_item.wert, any_order_dauerauftrag().wert);
        assert_eq!(result.default_item.konto, any_order_dauerauftrag().konto);
        assert_eq!(
            result.default_item.depotwert,
            any_order_dauerauftrag().depotwert
        );
        assert_eq!(
            result.default_item.start_datum,
            any_order_dauerauftrag().start_datum
        );
        assert_eq!(
            result.default_item.ende_datum,
            any_order_dauerauftrag().ende_datum
        );
        assert_eq!(
            result.default_item.rhythmus,
            any_order_dauerauftrag().rhythmus
        );

        assert_eq!(result.action_title, "Order-Dauerauftrag bearbeiten");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_should_preset_changes() {
        let database = generate_empty_database();
        let changes = vec![OrderDauerauftragChange {
            icon: PLUS,
            name: demo_name(),
            start_datum: demo_datum(),
            ende_datum: demo_datum(),
            rhythmus: Rhythmus::Monatlich,
            konto: demo_konto_referenz(),
            depotwert: demo_depotwert_referenz(),
            wert: demo_order_betrag(),
        }];
        let context = AddOrderDauerauftragContext {
            database: &database,
            edit_buchung: None,
            order_dauerauftrag_changes: &changes,
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
        let context = AddOrderDauerauftragContext {
            database: &database,
            edit_buchung: None,
            order_dauerauftrag_changes: &vec![],
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

        let context = AddOrderDauerauftragContext {
            database: &database,
            edit_buchung: None,
            order_dauerauftrag_changes: &vec![],
            heute: demo_datum(),
        };

        let result = super::handle_view(context);

        assert_eq!(result.depotwerte.len(), 1);
        assert_eq!(result.depotwerte[0].value, "demoisin");
        assert_eq!(result.depotwerte[0].description, "demoname (demoisin)");
    }
}
