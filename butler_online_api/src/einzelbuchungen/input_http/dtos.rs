use crate::einzelbuchungen::model::{Einzelbuchung, NeueEinzelbuchung};
use bigdecimal::BigDecimal;
use serde::{Deserialize, Serialize};
use time::macros::format_description;
use time::Date;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NeueEinzelbuchungDto {
    pub name: String,
    pub kategorie: String,
    pub datum: String,
    pub wert: BigDecimal,
}

impl NeueEinzelbuchungDto {
    pub fn to_domain(&self, user: String) -> NeueEinzelbuchung {
        NeueEinzelbuchung {
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            datum: Date::parse(
                self.datum.as_str(),
                format_description!("[year]-[month]-[day]"),
            )
            .unwrap(),
            user,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct EinzelbuchungDto {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub datum: String,
    pub user: String,
}

impl Einzelbuchung {
    pub fn to_dto(&self) -> EinzelbuchungDto {
        EinzelbuchungDto {
            datum: self.datum.to_string(),
            id: self.id.clone(),
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            user: self.user.clone(),
        }
    }
}
