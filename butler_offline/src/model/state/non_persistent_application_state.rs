use crate::budgetbutler::view::icons::Icon;
use crate::model::database::depotwert::{DepotwertReferenz, DepotwertTyp};
use crate::model::database::sparbuchung::{KontoReferenz, SparbuchungTyp};
use crate::model::database::sparkonto::Kontotyp;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::order_betrag::OrderBetrag;
use crate::model::primitives::person::Person;
use crate::model::primitives::rhythmus::Rhythmus;
use crate::model::state::persistent_state::database_version::DatabaseVersion;
use std::path::PathBuf;
use std::sync::Mutex;

pub struct EinzelbuchungenChanges {
    pub changes: Mutex<Vec<EinzelbuchungChange>>,
}

pub struct EinzelbuchungChange {
    pub icon: String,
    pub datum: Datum,
    pub name: Name,
    pub kategorie: Kategorie,
    pub betrag: Betrag,
}

pub struct GemeinsameBuchungenChanges {
    pub changes: Mutex<Vec<GemeinsameBuchungChange>>,
}

pub struct GemeinsameBuchungChange {
    pub icon: String,
    pub datum: Datum,
    pub name: Name,
    pub kategorie: Kategorie,
    pub betrag: Betrag,
    pub person: Person,
}

pub struct OnlineRedirectState {
    pub redirect_state: Mutex<OnlineRedirectActionWrapper>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct OnlineRedirectActionWrapper {
    pub action: Option<OnlineRedirectAction>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct OnlineRedirectAction {
    pub typ: OnlineRedirectActionType,
    pub database_version: DatabaseVersion,
}

#[derive(Debug, Clone, PartialEq)]
pub enum OnlineRedirectActionType {
    ImportEinzelbuchungen,
    UploadKategorien,
    ImportGemeinsameBuchungen,
    UploadGemeinsameBuchungen,
}

pub struct DauerauftraegeChanges {
    pub changes: Mutex<Vec<DauerauftragChange>>,
}

pub struct DauerauftragChange {
    pub icon: String,
    pub start_datum: Datum,
    pub ende_datum: Datum,
    pub rhythmus: Rhythmus,
    pub name: Name,
    pub kategorie: Kategorie,
    pub betrag: Betrag,
}

pub struct AdditionalKategorie {
    pub kategorie: Mutex<Option<Kategorie>>,
}

pub struct RootPath {
    pub path: PathBuf,
}

pub struct KontoChanges {
    pub changes: Mutex<Vec<KontoChange>>,
}

pub struct KontoChange {
    pub icon: String,
    pub name: Name,
    pub typ: Kontotyp,
}

pub struct SparbuchungenChanges {
    pub changes: Mutex<Vec<SparbuchungChange>>,
}

pub struct SparbuchungChange {
    pub icon: Icon,
    pub name: Name,
    pub datum: Datum,
    pub wert: BetragOhneVorzeichen,
    pub typ: SparbuchungTyp,
    pub konto: KontoReferenz,
}

pub struct DepotwerteChanges {
    pub changes: Mutex<Vec<DepotwertChange>>,
}

pub struct DepotwertChange {
    pub icon: Icon,
    pub name: Name,
    pub isin: ISIN,
    pub typ: DepotwertTyp,
}

pub struct OrderChanges {
    pub changes: Mutex<Vec<OrderChange>>,
}

pub struct OrderChange {
    pub icon: Icon,
    pub datum: Datum,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwert: DepotwertReferenz,
    pub wert: OrderBetrag,
}

pub struct OrderDauerauftragChanges {
    pub changes: Mutex<Vec<OrderDauerauftragChange>>,
}

pub struct OrderDauerauftragChange {
    pub icon: Icon,
    pub start_datum: Datum,
    pub ende_datum: Datum,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwert: DepotwertReferenz,
    pub wert: OrderBetrag,
    pub rhythmus: Rhythmus,
}

pub struct DepotauszuegeChanges {
    pub changes: Mutex<Vec<DepotauszugChange>>,
}

pub struct DepotauszugChange {
    pub icon: Icon,
    pub datum: Datum,
    pub konto: KontoReferenz,
    pub changes: Vec<DepotauszugSingleChange>,
}

pub struct DepotauszugSingleChange {
    pub depotwert_beschreibung: String,
    pub wert: Betrag,
}
