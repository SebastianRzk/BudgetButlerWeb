use crate::io::disk::database::types::ElementRequirement;
use crate::model::eigenschaften::besitzt_betrag::BesitztBetrag;
use crate::model::eigenschaften::besitzt_datum::BesitztDatum;
use crate::model::eigenschaften::besitzt_kategorie::BesitztKategorie;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Einzelbuchung {
    pub datum: Datum,
    pub name: Name,
    pub kategorie: Kategorie,
    pub betrag: Betrag,
}

impl ElementRequirement for Einzelbuchung {}

impl<'a> BesitztDatum<'a> for Einzelbuchung {
    fn datum(&'a self) -> &'a Datum {
        &self.datum
    }
}

impl<'a> BesitztDatum<'a> for Indiziert<Einzelbuchung> {
    fn datum(&'a self) -> &'a Datum {
        &self.value.datum
    }
}

impl<'a> BesitztKategorie<'a> for Indiziert<Einzelbuchung> {
    fn kategorie(&'a self) -> &'a Kategorie {
        &self.value.kategorie
    }
}

impl<'a> BesitztBetrag<'a> for Einzelbuchung {
    fn betrag(&'a self) -> &'a Betrag {
        &self.betrag
    }
}

impl<'a> BesitztBetrag<'a> for Indiziert<Einzelbuchung> {
    fn betrag(&'a self) -> &'a Betrag {
        &self.value.betrag
    }
}

impl<'a> BesitztBetrag<'a> for &Indiziert<Einzelbuchung> {
    fn betrag(&'a self) -> &'a Betrag {
        &self.value.betrag
    }
}

impl PartialOrd<Self> for Einzelbuchung {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Einzelbuchung {
    fn cmp(&self, other: &Self) -> Ordering {
        let ordering = self.datum.cmp(&other.datum);
        if ordering == Ordering::Equal {
            self.kategorie.cmp(&other.kategorie)
        } else {
            ordering
        }
    }
}

impl Einzelbuchung {
    pub fn change_kategorie(&self, neue_kategorie: Kategorie) -> Einzelbuchung {
        Einzelbuchung {
            datum: self.datum.clone(),
            name: self.name.clone(),
            kategorie: neue_kategorie,
            betrag: self.betrag.clone(),
        }
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::primitives::betrag::builder::any_betrag;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::kategorie::{kategorie, SPAREN_KATEGORIE};
    use crate::model::primitives::name::builder::demo_name;

    pub fn einzelbuchung_with_datum(vor_sechs_monaten: Datum) -> Einzelbuchung {
        Einzelbuchung {
            datum: vor_sechs_monaten,
            name: demo_name(),
            kategorie: demo_kategorie(),
            betrag: any_betrag(),
        }
    }

    pub fn einzelbuchung_with_betrag(betrag: Betrag) -> Einzelbuchung {
        Einzelbuchung {
            datum: any_datum(),
            name: demo_name(),
            kategorie: demo_kategorie(),
            betrag,
        }
    }

    pub fn sparbuchung_with_datum_und_betrag(datum: Datum, betrag: Betrag) -> Einzelbuchung {
        Einzelbuchung {
            datum,
            name: demo_name(),
            kategorie: kategorie(SPAREN_KATEGORIE),
            betrag,
        }
    }

    pub fn einzelbuchung_with_datum_und_betrag(datum: Datum, betrag: Betrag) -> Einzelbuchung {
        Einzelbuchung {
            datum,
            name: demo_name(),
            kategorie: demo_kategorie(),
            betrag,
        }
    }

    pub fn einzelbuchung_with_kategorie_und_betrag(
        kategorie_: &str,
        betrag: Betrag,
    ) -> Einzelbuchung {
        Einzelbuchung {
            datum: any_datum(),
            name: demo_name(),
            kategorie: kategorie(kategorie_),
            betrag,
        }
    }

    pub fn einzelbuchung_with_kategorie(kategorie_: &str) -> Einzelbuchung {
        Einzelbuchung {
            datum: any_datum(),
            name: demo_name(),
            kategorie: kategorie(kategorie_),
            betrag: any_betrag(),
        }
    }

    pub fn demo_einzelbuchung() -> Einzelbuchung {
        Einzelbuchung {
            datum: any_datum(),
            name: demo_name(),
            kategorie: demo_kategorie(),
            betrag: any_betrag(),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::einzelbuchung::builder::{
        einzelbuchung_with_datum, einzelbuchung_with_kategorie,
    };
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use std::cmp::Ordering;

    #[test]
    fn test_sort_by_date() {
        let left = einzelbuchung_with_datum(Datum::new(2, 1, 2024));
        let right = einzelbuchung_with_datum(Datum::new(1, 1, 2024));

        assert_eq!(left.cmp(&right), Ordering::Greater);
    }

    #[test]
    fn test_sort_by_kategorie() {
        let left = einzelbuchung_with_kategorie("A");
        let right = einzelbuchung_with_kategorie("B");

        assert_eq!(left.cmp(&right), Ordering::Less);
    }

    #[test]
    fn test_change_kategorie() {
        let original = einzelbuchung_with_kategorie("A");
        let neue_kategorie = "B";
        let expected = einzelbuchung_with_kategorie(neue_kategorie);

        let result = original.change_kategorie(kategorie(neue_kategorie));

        assert_eq!(result, expected);
    }
}
