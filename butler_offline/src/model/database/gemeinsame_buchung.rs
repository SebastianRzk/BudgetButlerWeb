use crate::io::disk::database::types::ElementRequirement;
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

impl ElementRequirement for GemeinsameBuchung {}

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

impl GemeinsameBuchung {
    pub fn change_kategorie(&self, neue_kategorie: Kategorie) -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum: self.datum.clone(),
            name: self.name.clone(),
            kategorie: neue_kategorie,
            betrag: self.betrag.clone(),
            person: self.person.clone(),
        }
    }

    pub fn change_person(&self, neue_person: Person) -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum: self.datum.clone(),
            name: self.name.clone(),
            kategorie: self.kategorie.clone(),
            betrag: self.betrag.clone(),
            person: neue_person,
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
    use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::primitives::betrag::builder::any_betrag;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::person::builder::demo_person;
    use crate::model::primitives::person::Person;

    pub fn demo_gemeinsame_buchung() -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum: any_datum(),
            name: demo_name(),
            kategorie: demo_kategorie(),
            betrag: any_betrag(),
            person: demo_person(),
        }
    }

    pub fn gemeinsame_buchung_mit_betrag(betrag: Betrag) -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum: any_datum(),
            name: demo_name(),
            kategorie: demo_kategorie(),
            betrag,
            person: demo_person(),
        }
    }

    pub fn gemeinsame_buchung(datum: Datum, person: Person, betrag: Betrag) -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum,
            name: demo_name(),
            kategorie: demo_kategorie(),
            betrag,
            person,
        }
    }

    pub fn gemeinsame_buchung_mit_person(person: &str) -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum: any_datum(),
            name: demo_name(),
            kategorie: demo_kategorie(),
            betrag: any_betrag(),
            person: Person::new(person.to_string()),
        }
    }

    pub fn gemeinsame_buchung_mit_kategorie(neue_kategorie: &str) -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum: any_datum(),
            name: demo_name(),
            kategorie: kategorie(neue_kategorie),
            betrag: any_betrag(),
            person: demo_person(),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::gemeinsame_buchung::builder::demo_gemeinsame_buchung;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::person::builder::person;

    #[test]
    fn test_change_kategorie() {
        let gemeinsame_buchung = demo_gemeinsame_buchung();
        let neue_kategorie = kategorie("Neue Kategorie");

        let result = gemeinsame_buchung.change_kategorie(neue_kategorie.clone());

        assert_eq!(result.kategorie, neue_kategorie);
    }

    #[test]
    fn test_change_person() {
        let gemeinsame_buchung = demo_gemeinsame_buchung();
        let neue_person = person("Neue Person");

        let result = gemeinsame_buchung.change_person(neue_person.clone());

        assert_eq!(result.person, neue_person);
    }

    #[test]
    fn test_change_kategorie_gemeinsame_buchung() {
        let gemeinsame_buchung = demo_gemeinsame_buchung();
        let neue_kategorie = kategorie("Neue Kategorie");

        let result = gemeinsame_buchung.change_kategorie(neue_kategorie.clone());

        assert_eq!(result.kategorie, neue_kategorie);
    }
}
