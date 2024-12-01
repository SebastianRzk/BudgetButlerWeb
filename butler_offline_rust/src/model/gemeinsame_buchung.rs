use crate::model::eigenschaften::besitzt_betrag::BesitztBetrag;
use crate::model::eigenschaften::besitzt_datum::BesitztDatum;
use crate::model::eigenschaften::besitzt_person::BesitztPerson;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::person::Person;
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GemeinsameBuchung {
    pub datum: Datum,
    pub name: Name,
    pub kategorie: Kategorie,
    pub betrag: Betrag,
    pub person: Person,
}

impl PartialOrd<Self> for GemeinsameBuchung {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for GemeinsameBuchung {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        let ordering = self.datum.cmp(&other.datum);
        if ordering == Ordering::Equal {
            self.kategorie.cmp(&other.kategorie)
        } else {
            ordering
        }
    }
}

impl<'a> BesitztDatum<'a> for Indiziert<GemeinsameBuchung> {
    fn datum(&'a self) -> &'a Datum {
        &self.value.datum
    }
}

impl<'a> BesitztPerson<'a> for Indiziert<GemeinsameBuchung> {
    fn person(&'a self) -> &'a Person {
        &self.value.person
    }
}

impl<'a> BesitztBetrag<'a> for GemeinsameBuchung {
    fn betrag(&'a self) -> &'a Betrag {
        &self.betrag
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::primitives::betrag::builder::any_betrag;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::builder::any_kategorie;
    use crate::model::primitives::name::builder::any_name;
    use crate::model::primitives::person::builder::any_person;
    use crate::model::primitives::person::Person;

    pub fn any_gemeinsame_buchung() -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum: any_datum(),
            name: any_name(),
            kategorie: any_kategorie(),
            betrag: any_betrag(),
            person: any_person(),
        }
    }

    pub fn gemeinsame_buchung_mit_betrag(betrag: Betrag) -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum: any_datum(),
            name: any_name(),
            kategorie: any_kategorie(),
            betrag,
            person: any_person(),
        }
    }

    pub fn gemeinsame_buchung(datum: Datum, person: Person, betrag: Betrag) -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum,
            name: any_name(),
            kategorie: any_kategorie(),
            betrag,
            person,
        }
    }

    pub fn gemeinsame_buchung_mit_person(person: &str) -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum: any_datum(),
            name: any_name(),
            kategorie: any_kategorie(),
            betrag: any_betrag(),
            person: Person::new(person.to_string()),
        }
    }
}
