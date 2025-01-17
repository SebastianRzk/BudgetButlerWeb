use crate::model::primitives::datum::Datum;
use chrono::{Datelike, Local};

pub fn today() -> Datum {
    let time = Local::now();
    Datum::new(time.day(), time.month(), time.year())
}

pub fn now() -> String {
    let time = Local::now();
    format!("{}", time.timestamp())
}
