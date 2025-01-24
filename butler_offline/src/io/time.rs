use crate::model::primitives::datum::Datum;
use chrono::{Local};

#[cfg(not(feature = "integration_test"))]
pub fn today() -> Datum {
    let time = Local::now();
    Datum::new(time.day(), time.month(), time.year())
}

#[cfg(feature = "integration_test")]
pub fn today() -> Datum {
    Datum::new(22, 1, 2019)
}

pub fn now() -> String {
    let time = Local::now();
    format!("{}", time.timestamp())
}
