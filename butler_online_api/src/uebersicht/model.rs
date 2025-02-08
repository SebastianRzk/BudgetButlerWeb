use crate::einzelbuchungen::model::Einzelbuchung;
use crate::gemeinsame_buchungen::model::GemeinsameBuchung;
use bigdecimal::BigDecimal;
use std::collections::HashMap;

pub struct Uebersicht {
    pub monate: Vec<MonatsUebersicht>,
}

pub struct MonatsUebersicht {
    pub name: String,
    pub werte: HashMap<String, BigDecimal>,
}

pub trait BesitztDatumKategorieUndBetrag {
    fn get_datum(&self) -> &time::Date;
    fn get_kategorie(&self) -> &String;
    fn get_betrag(&self) -> &BigDecimal;
}

impl BesitztDatumKategorieUndBetrag for Einzelbuchung {
    fn get_datum(&self) -> &time::Date {
        &self.datum
    }

    fn get_betrag(&self) -> &BigDecimal {
        &self.wert
    }

    fn get_kategorie(&self) -> &String {
        &self.kategorie
    }
}

impl BesitztDatumKategorieUndBetrag for GemeinsameBuchung {
    fn get_datum(&self) -> &time::Date {
        &self.datum
    }

    fn get_betrag(&self) -> &BigDecimal {
        &self.wert
    }

    fn get_kategorie(&self) -> &String {
        &self.kategorie
    }
}
