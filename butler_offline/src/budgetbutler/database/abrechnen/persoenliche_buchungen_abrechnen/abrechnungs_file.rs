use crate::io::disk::diskrepresentation::line::Line;

pub struct SortedAbrechnungsFile {
    pub beschreibung: Vec<Line>,
    pub metadaten: Vec<Line>,
    pub einzel_buchungen: Vec<Line>,
    pub gemeinsame_buchungen: Vec<Line>,
}

pub const METADATEN_START: &str = "#######MaschinenimportMetadatenStart";
pub const METADATEN_END: &str = "#######MaschinenimportMetadatenEnd";
pub const BUCHUNGEN_START: &str = "#######MaschinenimportStart";
pub const BUCHUNGEN_END: &str = "#######MaschinenimportEnd";
pub const BUCHUNGEN_EINZEL_HEADER: &str = "Datum,Kategorie,Name,Betrag";
pub const BUCHUNGEN_GEMEINSAM_HEADER: &str = "Datum,Kategorie,Name,Betrag,Person";

pub const METADATEN_ABRECHNUNGSDATUM_KEY: &str = "Abrechnungsdatum:";
pub const METADATEN_ABRECHNENDE_PERSON_KEY: &str = "Abrechnende Person:";
pub const METADATEN_TITEL_KEY: &str = "Titel:";
pub const METADATEN_ZIEL_KEY: &str = "Ziel:";
pub const METADATEN_AUSFUEHRUNGSDATUM_KEY: &str = "Ausfuehrungsdatum:";

pub const ZIEL_IMPORT_GEMEINSAME_BUCHUNGEN_AUS_APP: &str = "ImportGemeinsamerBuchungenAusApp";
pub const ZIEL_ABRECHNUNG_SELBST: &str = "GemeinsameAbrechnungFuerSelbst";
pub const ZIEL_ABRECHNUNG_PARTNER: &str = "GemeinsameAbrechnungFuerPartner";
pub const ZIEL_IMPORT_EINZELBUCHUNGEN: &str = "ImportBuchungenAusApp";
