use bigdecimal::BigDecimal;
use time::Date;

pub struct NeueEinzelbuchung {
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub datum: Date,
    pub user: String,
}

pub struct Einzelbuchung {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub datum: Date,
    pub user: String,
}
