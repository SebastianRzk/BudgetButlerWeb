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


#[cfg(test)]
pub mod builder {
    use crate::model::einzelbuchung::Einzelbuchung;
    use crate::model::primitives::betrag::builder::any_betrag;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::builder::any_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::builder::any_name;

    pub fn to_einzelbuchung_with_datum(vor_sechs_monaten: Datum) -> Einzelbuchung {
        Einzelbuchung {
            datum: vor_sechs_monaten,
            name: any_name(),
            kategorie: any_kategorie(),
            betrag: any_betrag(),
        }
    }


    pub fn to_einzelbuchung_with_betrag(betrag: Betrag) -> Einzelbuchung {
        Einzelbuchung {
            datum: any_datum(),
            name: any_name(),
            kategorie: any_kategorie(),
            betrag,
        }
    }

    pub fn to_einzelbuchung_with_datum_and_betrag(vor_sechs_monaten: Datum, betrag: Betrag) -> Einzelbuchung {
        Einzelbuchung {
            datum: vor_sechs_monaten,
            name: any_name(),
            kategorie: any_kategorie(),
            betrag,
        }
    }

    pub fn to_einzelbuchung_with_kategorie_und_betrag(kategorie_: &str, betrag: Betrag) -> Einzelbuchung {
        Einzelbuchung {
            datum: any_datum(),
            name: any_name(),
            kategorie: kategorie(kategorie_),
            betrag,
        }
    }

    pub fn to_einzelbuchung_with_kategorie(kategorie_: &str) -> Einzelbuchung {
        Einzelbuchung {
            datum: any_datum(),
            name: any_name(),
            kategorie: kategorie(kategorie_),
            betrag: any_betrag(),
        }
    }

    pub fn any_einzelbuchung() -> Einzelbuchung {
        Einzelbuchung {
            datum: any_datum(),
            name: any_name(),
            kategorie: any_kategorie(),
            betrag: any_betrag(),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::model::einzelbuchung::builder::{to_einzelbuchung_with_datum, to_einzelbuchung_with_kategorie};
    use crate::model::primitives::datum::Datum;
    use std::cmp::Ordering;

    #[test]
    fn test_sort_by_date() {
        let left = to_einzelbuchung_with_datum(Datum::new(2, 1, 2024));
        let right = to_einzelbuchung_with_datum(Datum::new(1, 1, 2024));

        assert_eq!(left.cmp(&right), Ordering::Greater);
    }

    #[test]
    fn test_sort_by_kategorie() {
        let left = to_einzelbuchung_with_kategorie("A");
        let right = to_einzelbuchung_with_kategorie("B");

        assert_eq!(left.cmp(&right), Ordering::Less);
    }
}