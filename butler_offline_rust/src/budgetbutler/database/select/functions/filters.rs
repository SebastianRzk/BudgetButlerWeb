use crate::model::eigenschaften::besitzt_betrag::BesitztBetrag;
use crate::model::eigenschaften::besitzt_datum::BesitztDatum;
use crate::model::eigenschaften::besitzt_person::BesitztPerson;
use crate::model::primitives::betrag::Vorzeichen;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::person::Person;

pub fn filter_die_letzten_6_monate<T: for<'a> BesitztDatum<'a>>(heute: Datum) -> impl Fn(&T) -> bool {
    let vor_sechs_monaten = heute.substract_months(6).clamp_to_first_of_month();
    move |item: &T| -> bool {
        item.datum() >= &vor_sechs_monaten
    }
}

pub fn filter_auf_zeitraum<T: for<'a> BesitztDatum<'a>>(start: Datum, ende: Datum) -> impl Fn(&T) -> bool {
    move |item: &T| -> bool {
        item.datum() >= &start && item.datum() <= &ende
    }
}

pub fn filter_den_aktuellen_monat<T: for<'a> BesitztDatum<'a>>(heute: Datum) -> impl Fn(&T) -> bool {
    move |item: &T| -> bool {
        item.datum().monat == heute.monat && item.datum().jahr == heute.jahr
    }
}

pub fn filter_auf_das_jahr<T: for<'a> BesitztDatum<'a>>(jahr: i32) -> impl Fn(&T) -> bool {
    move |item: &T| -> bool {
        item.datum().jahr == jahr
    }
}

pub fn filter_auf_jahr_und_monat<T: for<'a> BesitztDatum<'a>>(jahr: i32, monat: u32) -> impl Fn(&T) -> bool {
    move |item: &T| -> bool {
        item.datum().jahr == jahr && item.datum().monat == monat
    }
}

pub fn filter_auf_einnahmen<T: for<'a> BesitztBetrag<'a>>(item: &T) -> bool {
    item.betrag().vorzeichen == Vorzeichen::Positiv
}

pub fn filter_auf_ausgaben<T: for<'a> BesitztBetrag<'a>>(item: &T) -> bool {
    item.betrag().vorzeichen == Vorzeichen::Negativ
}

pub fn filter_auf_person<T: for<'a> BesitztPerson<'a>>(person: Person) -> impl Fn(&T) -> bool {
    move |item: &T| -> bool {
        item.person() == &person
    }
}


#[cfg(test)]
mod tests {
    use super::{filter_auf_ausgaben, filter_auf_einnahmen, filter_auf_zeitraum};
    use crate::budgetbutler::database::select::functions::filters::{filter_auf_das_jahr, filter_auf_jahr_und_monat, filter_den_aktuellen_monat, filter_die_letzten_6_monate};
    use crate::model::einzelbuchung::builder::{to_einzelbuchung_with_betrag, to_einzelbuchung_with_datum};
    use crate::model::gemeinsame_buchung::builder::gemeinsame_buchung_mit_person;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::person::Person;

    #[test]
    fn test_filter_die_letzten_6_monate() {
        let heute = Datum::new(1, 1, 2020);

        let filter = filter_die_letzten_6_monate(heute);

        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(1, 7, 2019))), true);
        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(2, 7, 2019))), true);
        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(30, 6, 2019))), false);
    }

    #[test]
    fn test_filter_den_aktuellen_monat() {
        let heute = Datum::new(1, 1, 2020);

        let filter = filter_den_aktuellen_monat(heute);

        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(1, 1, 2020))), true);
        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(2, 1, 2020))), true);
        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(30, 6, 2019))), false);
    }

    #[test]
    fn test_filter_auf_das_jahr() {
        let filter = filter_auf_das_jahr(2020);

        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(1, 1, 2020))), true);
        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(2, 1, 2020))), true);
        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(30, 6, 2019))), false);
    }

    #[test]
    fn test_filter_auf_jahr_und_monat() {
        let filter = filter_auf_jahr_und_monat(2020, 1);

        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(1, 1, 2020))), true);
        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(2, 1, 2020))), true);
        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(30, 6, 2019))), false);
    }

    #[test]
    fn test_filter_auf_einnahmen() {
        assert_eq!(filter_auf_einnahmen(&to_einzelbuchung_with_betrag(Betrag::from_user_input(&"-2".to_string()))), false);
        assert_eq!(filter_auf_einnahmen(&to_einzelbuchung_with_betrag(Betrag::from_user_input(&"2".to_string()))), true);
    }

    #[test]
    fn test_filter_auf_ausgaben() {
        assert_eq!(filter_auf_ausgaben(&to_einzelbuchung_with_betrag(Betrag::from_user_input(&"-2".to_string()))), true);
        assert_eq!(filter_auf_ausgaben(&to_einzelbuchung_with_betrag(Betrag::from_user_input(&"2".to_string()))), false);
    }
    #[test]
    fn test_filter_auf_zeitraum() {
        let start = Datum::new(1, 1, 2020);
        let ende = Datum::new(31, 1, 2020);

        let filter = filter_auf_zeitraum(start, ende);

        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(1, 1, 2020))), true);
        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(31, 1, 2020))), true);
        assert_eq!(filter(&to_einzelbuchung_with_datum(Datum::new(30, 6, 2019))), false);
    }

    #[test]
    fn test_filter_auf_person(){
        let filter = super::filter_auf_person(Person::new("test_person".to_string()));
        assert_eq!(filter(&indiziert(gemeinsame_buchung_mit_person("other person"))), false);
        assert_eq!(filter(&indiziert(gemeinsame_buchung_mit_person("test_person"))), true);
    }
}