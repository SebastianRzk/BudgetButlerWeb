use crate::model::database::sparbuchung::{KontoReferenz, SparbuchungTyp};
use crate::model::database::sparkonto::Sparkonto;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::name::Name;
use crate::model::state::non_persistent_application_state::SparbuchungChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct AddSparbuchungenViewResult {
    pub database_version: DatabaseVersion,
    pub bearbeitungsmodus: bool,
    pub action_headline: String,
    pub default_item: DefaultItem,
    pub action_title: String,
    pub letzte_erfassungen: Vec<LetzteErfassung>,
    pub kontos: Vec<Indiziert<Sparkonto>>,
    pub typen: Vec<SparbuchungTyp>,
}

pub struct LetzteErfassung {
    pub icon: String,
    pub name: Name,
    pub datum: Datum,
    pub wert: BetragOhneVorzeichen,
    pub typ: SparbuchungTyp,
    pub konto: KontoReferenz,
}

pub struct AddSparbuchungenContext<'a> {
    pub database: &'a Database,
    pub sparbuchung_changes: &'a Vec<SparbuchungChange>,
    pub edit_buchung: Option<u32>,
    pub heute: Datum,
}

pub struct DefaultItem {
    pub index: u32,
    pub name: Name,
    pub datum: Datum,
    pub wert: BetragOhneVorzeichen,
    pub typ: SparbuchungTyp,
    pub konto: KontoReferenz,
}

pub fn handle_view(context: AddSparbuchungenContext) -> AddSparbuchungenViewResult {
    let mut default_item = DefaultItem {
        index: 0,
        name: Name::empty(),
        datum: context.heute,
        konto: KontoReferenz::new(Name::empty()),
        wert: BetragOhneVorzeichen::zero(),
        typ: SparbuchungTyp::ManuelleEinzahlung,
    };
    let mut action_headline = "Sparbuchung erfassen".to_string();
    let mut action_title = "Sparbuchung erfassen".to_string();
    let mut bearbeitungsmodus = false;

    if let Some(edit_index) = context.edit_buchung {
        let edit_buchung = context.database.sparbuchungen.get(edit_index);
        default_item = DefaultItem {
            index: edit_index,
            name: edit_buchung.value.name,
            datum: edit_buchung.value.datum,
            konto: edit_buchung.value.konto.clone(),
            wert: edit_buchung.value.wert,
            typ: edit_buchung.value.typ.clone(),
        };
        bearbeitungsmodus = true;
        action_headline = "Sparbuchung bearbeiten".to_string();
        action_title = "Sparbuchung bearbeiten".to_string();
    }

    let result = AddSparbuchungenViewResult {
        database_version: context.database.db_version.clone(),
        bearbeitungsmodus,
        action_headline,
        default_item,
        kontos: context.database.sparkontos.select().collect(),
        action_title,
        letzte_erfassungen: context
            .sparbuchung_changes
            .iter()
            .map(|change| LetzteErfassung {
                icon: change.icon.as_fa.to_string(),
                name: change.name.clone(),
                datum: change.datum.clone(),
                wert: change.wert.clone(),
                typ: change.typ.clone(),
                konto: change.konto.clone(),
            })
            .collect(),
        typen: vec![
            SparbuchungTyp::ManuelleEinzahlung,
            SparbuchungTyp::ManuelleAuszahlung,
            SparbuchungTyp::Ausschuettung,
            SparbuchungTyp::Zinsen,
            SparbuchungTyp::SonstigeKosten,
        ],
    };
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::add_sparbuchung::AddSparbuchungenContext;
    use crate::budgetbutler::view::icons::PLUS;
    use crate::model::database::sparbuchung::builder::{any_sparbuchung, konto_referenz};
    use crate::model::database::sparbuchung::SparbuchungTyp;
    use crate::model::database::sparkonto::builder::demo_konto;
    use crate::model::indiziert::Indiziert;
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::Name;
    use crate::model::state::non_persistent_application_state::SparbuchungChange;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_sparkontos, generate_database_with_sparkontos_und_sparbuchungen,
        generate_empty_database,
    };

    #[test]
    pub fn test_handle_view_without_edit_index() {
        let database = generate_database_with_sparkontos(vec![demo_konto()]);
        let context = AddSparbuchungenContext {
            database: &database,
            sparbuchung_changes: &vec![],
            edit_buchung: None,
            heute: Datum::new(1, 1, 2021),
        };

        let result = super::handle_view(context);

        assert_eq!(result.database_version.name, "empty");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.action_headline, "Sparbuchung erfassen");

        assert_eq!(result.default_item.index, 0);
        assert_eq!(result.default_item.name, Name::empty());
        assert_eq!(result.default_item.typ, SparbuchungTyp::ManuelleEinzahlung);
        assert_eq!(result.default_item.konto, konto_referenz(""));
        assert_eq!(result.default_item.wert, BetragOhneVorzeichen::zero());

        assert_eq!(
            result.typen,
            vec![
                SparbuchungTyp::ManuelleEinzahlung,
                SparbuchungTyp::ManuelleAuszahlung,
                SparbuchungTyp::Ausschuettung,
                SparbuchungTyp::Zinsen,
                SparbuchungTyp::SonstigeKosten,
            ]
        );

        assert_eq!(result.kontos.len(), 1);
        assert_eq!(
            result.kontos[0],
            Indiziert {
                index: 1,
                dynamisch: false,
                value: demo_konto(),
            }
        );

        assert_eq!(result.action_title, "Sparbuchung erfassen");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_with_edit_index() {
        let database = generate_database_with_sparkontos_und_sparbuchungen(
            vec![demo_konto()],
            vec![any_sparbuchung()],
        );
        let changes = vec![];
        let context = AddSparbuchungenContext {
            database: &database,
            edit_buchung: Some(2),
            sparbuchung_changes: &changes,
            heute: Datum::new(1, 1, 2021),
        };

        let result = super::handle_view(context);

        assert_eq!(result.database_version.as_string(), "empty-1-0");
        assert_eq!(result.bearbeitungsmodus, true);
        assert_eq!(result.action_headline, "Sparbuchung bearbeiten");

        assert_eq!(result.default_item.index, 2);
        assert_eq!(result.default_item.name, any_sparbuchung().name);
        assert_eq!(result.default_item.typ, any_sparbuchung().typ);
        assert_eq!(result.default_item.konto, any_sparbuchung().konto);
        assert_eq!(result.default_item.wert, any_sparbuchung().wert);

        assert_eq!(
            result.typen,
            vec![
                SparbuchungTyp::ManuelleEinzahlung,
                SparbuchungTyp::ManuelleAuszahlung,
                SparbuchungTyp::Ausschuettung,
                SparbuchungTyp::Zinsen,
                SparbuchungTyp::SonstigeKosten,
            ]
        );

        assert_eq!(result.kontos.len(), 1);
        assert_eq!(
            result.kontos[0],
            Indiziert {
                index: 1,
                dynamisch: false,
                value: demo_konto(),
            }
        );

        assert_eq!(result.action_title, "Sparbuchung bearbeiten");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_should_preset_changes() {
        let database = generate_empty_database();
        let changes = vec![SparbuchungChange {
            icon: PLUS,
            name: demo_konto().name,
            datum: Datum::new(1, 1, 2021),
            wert: BetragOhneVorzeichen::zero(),
            typ: SparbuchungTyp::ManuelleEinzahlung,
            konto: konto_referenz("kontoreferenz"),
        }];
        let context = AddSparbuchungenContext {
            database: &database,
            edit_buchung: None,
            sparbuchung_changes: &changes,
            heute: Datum::new(1, 1, 2021),
        };

        let result = super::handle_view(context);

        assert_eq!(result.letzte_erfassungen.len(), 1);
        assert_eq!(result.letzte_erfassungen[0].icon, "fa fa-plus");
        assert_eq!(result.letzte_erfassungen[0].name, demo_konto().name);
        assert_eq!(result.letzte_erfassungen[0].datum, Datum::new(1, 1, 2021));
        assert_eq!(
            result.letzte_erfassungen[0].wert,
            BetragOhneVorzeichen::zero()
        );
        assert_eq!(
            result.letzte_erfassungen[0].typ,
            SparbuchungTyp::ManuelleEinzahlung
        );
        assert_eq!(
            result.letzte_erfassungen[0].konto,
            konto_referenz("kontoreferenz")
        );
    }
}
