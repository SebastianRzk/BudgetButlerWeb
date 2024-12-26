use crate::core::rhythmus::Rhythmus;
use bigdecimal::BigDecimal;
use time::Date;

pub struct NeuerDauerauftrag {
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub start_datum: Date,
    pub ende_datum: Date,
    pub rhythmus: Rhythmus,
    pub user: String,
}

pub struct Dauerauftrag {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub start_datum: Date,
    pub ende_datum: Date,
    pub rhythmus: Rhythmus,
    pub letzte_ausfuehrung: Option<Date>,
    pub user: String,
}
