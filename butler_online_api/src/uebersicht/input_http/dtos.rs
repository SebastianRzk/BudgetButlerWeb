use crate::uebersicht::model::{
    GemeinsameMonatsuebersicht, GemeinsameUebersicht, MonatsUebersicht, Uebersicht,
};
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
    pub personen: Option<HashMap<String, BigDecimal>>,
    pub gesamt: BigDecimal,
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
            personen: None,
            gesamt: self.gesamt,
        }
    }
}

impl GemeinsameUebersicht {
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

impl GemeinsameMonatsuebersicht {
    pub fn to_dto(self) -> MonatsUebersichtDto {
        MonatsUebersichtDto {
            name: self.name,
            werte: self.werte,
            personen: Some(self.personen),
            gesamt: self.gesamt,
        }
    }
}
