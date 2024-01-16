use bigdecimal::BigDecimal;
use time::Date;

pub struct NeueGemeinsameBuchung {
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub datum: Date,
    pub user: String,
    pub zielperson: String,
}

pub struct GemeinsameBuchung {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub datum: Date,
    pub user: String,
    pub zielperson: String,
}
