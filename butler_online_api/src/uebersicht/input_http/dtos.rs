use crate::uebersicht::model::{MonatsUebersicht, Uebersicht};
use bigdecimal::BigDecimal;
use serde::Serialize;
use std::collections::HashMap;

#[derive(Serialize)]
pub struct UebersichtDto {
    pub monate: Vec<MonatsUebersichtDto>,
}

#[derive(Serialize)]
pub struct MonatsUebersichtDto {
    pub name: String,
    pub werte: HashMap<String, BigDecimal>,
}

impl Uebersicht {
    pub fn to_dto(self) -> UebersichtDto {
        UebersichtDto {
            monate: self
                .monate
                .into_iter()
                .map(|monat| monat.to_dto())
                .collect(),
        }
    }
}

impl MonatsUebersicht {
    pub fn to_dto(self) -> MonatsUebersichtDto {
        MonatsUebersichtDto {
            name: self.name,
            werte: self.werte,
        }
    }
}
