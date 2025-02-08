use chrono::Datelike;
use time::{Date, Month};

pub fn monats_name_from_datum(datum: &Date) -> String {
    format!("{} {}", monats_name(datum.month()), datum.year())
}

fn monats_name(month: Month) -> String {
    match month {
        Month::January => "Januar".to_string(),
        Month::February => "Februar".to_string(),
        Month::March => "März".to_string(),
        Month::April => "April".to_string(),
        Month::May => "Mai".to_string(),
        Month::June => "Juni".to_string(),
        Month::July => "Juli".to_string(),
        Month::August => "August".to_string(),
        Month::September => "September".to_string(),
        Month::October => "Oktober".to_string(),
        Month::November => "November".to_string(),
        Month::December => "Dezember".to_string(),
    }
}
