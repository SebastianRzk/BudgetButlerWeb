use crate::core::rhythmus::Rhythmus;
use bigdecimal::BigDecimal;
use time::Date;

pub struct NeuerGemeinsamerDauerauftrag {
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub start_datum: Date,
    pub ende_datum: Date,
    pub rhythmus: Rhythmus,
    pub user: String,
    pub zielperson: String,
}

pub struct GemeinsamerDauerauftrag {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub start_datum: Date,
    pub ende_datum: Date,
    pub rhythmus: Rhythmus,
    pub letzte_ausfuehrung: Option<Date>,
    pub user: String,
    pub zielperson: String,
}
