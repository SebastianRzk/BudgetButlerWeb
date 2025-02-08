use crate::einzelbuchungen::model::{Einzelbuchung, NeueEinzelbuchung};
use crate::schema::einzelbuchungen;
use bigdecimal::BigDecimal;
use diesel::{Insertable, Queryable};
use serde::{Deserialize, Serialize};
use time::Date;

#[derive(Debug, Clone, Serialize, Deserialize, Queryable, Insertable)]
#[diesel(table_name = einzelbuchungen)]
pub struct EinzelbuchungEntity {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub datum: Date,
    pub user: String,
}

impl NeueEinzelbuchung {
    pub fn to_entity(self, id: String) -> EinzelbuchungEntity {
        EinzelbuchungEntity {
            id,
            name: self.name.clone(),
            kategorie: self.kategorie.clone(),
            wert: self.wert,
            datum: self.datum,
            user: self.user.clone(),
        }
    }
}

impl EinzelbuchungEntity {
    pub fn to_domain(&self) -> Einzelbuchung {
        Einzelbuchung {
            datum: self.datum.clone(),
            id: self.id.clone(),
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            user: self.user.clone(),
        }
    }
}
