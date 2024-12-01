use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::person::Person;
use crate::model::primitives::rhythmus::Rhythmus;
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
    pub person: Person
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
