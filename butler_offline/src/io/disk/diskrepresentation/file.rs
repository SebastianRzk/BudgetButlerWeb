use crate::io::disk::diskrepresentation::line::Line;

pub struct File {
    pub lines: Vec<Line>,
}

pub struct SortedFile {
    pub einzelbuchungen: Vec<Line>,
    pub dauerauftraege: Vec<Line>,
    pub gemeinsame_buchungen: Vec<Line>,
    pub sparbuchungen: Vec<Line>,
    pub sparkontos: Vec<Line>,
    pub depotwerte: Vec<Line>,
    pub order: Vec<Line>,
    pub order_dauerauftrag: Vec<Line>,
    pub depotauszuege: Vec<Line>,
}

pub const EINZELBUCHUNGEN_HEADER: &str = "Datum,Kategorie,Name,Wert";

pub const DAUERAUFTRAEGE_START_SIGNAL: &str = "Dauerauftraege";
pub const DAUERAUFTRAEGE_HEADER: &str = "Startdatum,Endedatum,Kategorie,Name,Rhythmus,Wert";

pub const GEMEINSAME_BUCHUGEN_START_SIGNAL: &str = "Gemeinsame Buchungen";
pub const GEMEINSAME_BUCHUGEN_HEADER: &str = "Datum,Kategorie,Name,Wert,Person";

pub const SPARBUCHUNGEN_START_SIGNAL: &str = "Sparbuchungen";
pub const SPARBUCHUNGEN_HEADER: &str = "Datum,Name,Wert,Typ,Konto";

pub const SPARKONTOS_START_SIGNAL: &str = "Sparkontos";
pub const SPARKONTOS_HEADER: &str = "Kontoname,Kontotyp";

pub const DEPOTWERTE_START_SIGNAL: &str = "Depotwerte";
pub const DEPOTWERTE_HEADER: &str = "Name,ISIN,Typ";

pub const ORDER_START_SIGNAL: &str = "Order";
pub const ORDER_HEADER: &str = "Datum,Name,Konto,Depotwert,Wert,Typ";

pub const DAUERAUFTRAG_ORDER_START_SIGNAL: &str = "Dauerauftr_Ordr";
pub const DAUERAUFTRAG_ORDER_HEADER: &str =
    "Startdatum,Endedatum,Rhythmus,Name,Konto,Depotwert,Wert,Typ";

pub const DEPOTAUSZUEGE_START_SIGNAL: &str = "Depotauszuege";
pub const DEPOTAUSZUEGE_HEADER: &str = "Datum,Depotwert,Konto,Wert";

#[cfg(test)]
pub mod builder {
    use crate::io::disk::diskrepresentation::file::File;
    use crate::io::disk::diskrepresentation::line::builder::line;

    impl File {
        pub fn from_str(file: &str) -> File {
            let lines = file.lines().map(|l| line(l)).collect();
            File { lines }
        }
    }
}
