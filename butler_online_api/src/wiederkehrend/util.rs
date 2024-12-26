use crate::core::rhythmus::Rhythmus;
use chrono::Datelike;
use chrono::NaiveDate;
use time::{Date, Month};

pub fn get_days_from_month(year: i32, month: u32) -> i64 {
    NaiveDate::from_ymd_opt(
        match month {
            12 => year + 1,
            _ => year,
        },
        match month {
            12 => 1,
            _ => month + 1,
        },
        1,
    )
    .unwrap()
    .signed_duration_since(NaiveDate::from_ymd_opt(year, month, 1).unwrap())
    .num_days()
}

fn add_one_month(date: Date, months_to_add: u32) -> Date {
    let month_number = date.month() as i32;
    let additional_years = (month_number.clone() - (month_number.clone() % 12)) / 12;
    let max_days_of_month = get_days_from_month(
        date.year() + additional_years,
        date.month().nth_next(months_to_add as u8) as u32,
    );
    let mut days = date.day() as i64;
    if days > max_days_of_month.clone() {
        days = max_days_of_month;
    }

    return Date::from_calendar_date(
        date.year() + additional_years,
        date.month().nth_next(months_to_add as u8),
        days as u8,
    )
    .unwrap();
}

pub fn to_date(date_like: NaiveDate) -> Date {
    Date::from_calendar_date(
        date_like.year(),
        Month::January.nth_next((date_like.month() - 1) as u8),
        date_like.day() as u8,
    )
    .unwrap()
}

pub fn calculate_naechste_buchung(
    start_datum: Date,
    letzte_ausfuehrung: Option<Date>,
    rhythmus: Rhythmus,
) -> Date {
    let mut naechste_buchung = start_datum;
    if letzte_ausfuehrung.is_some() {
        naechste_buchung = compute_next_date(letzte_ausfuehrung.unwrap(), rhythmus);
    }
    naechste_buchung
}

pub fn compute_next_date(letztes_datum: Date, rhythmus: Rhythmus) -> Date {
    match rhythmus {
        Rhythmus::Monatlich => add_one_month(letztes_datum, 1),
        Rhythmus::ViertelJaehrlich => add_one_month(letztes_datum, 3),
        Rhythmus::HalbJaehrlich => add_one_month(letztes_datum, 6),
        Rhythmus::Jaehrlich => add_one_month(letztes_datum, 12),
    }
}
