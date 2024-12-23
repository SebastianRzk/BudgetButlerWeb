use crate::model::primitives::betrag::{Betrag, Vorzeichen};
use crate::model::primitives::datum::MonatsName;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use std::cmp::Ordering;
use std::collections::HashMap;
use std::ops::Add;

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
pub struct MonatsAggregationsIndex {
    pub monat: u32,
    pub jahr: i32,
}

#[derive(Debug, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct JahresAggregationsIndex {
    pub jahr: i32,
}

#[derive(Debug, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct TagesAggregationsIndex {
    pub tag: u32,
}

impl PartialOrd<Self> for MonatsAggregationsIndex {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for MonatsAggregationsIndex {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.jahr == other.jahr {
            self.monat.cmp(&other.monat)
        } else {
            self.jahr.cmp(&other.jahr)
        }
    }
}

impl MonatsAggregationsIndex {
    pub fn format_descriptive_string(&self) -> MonatsName {
        MonatsName {
            monat: format!("{:02}/{}", self.monat, self.jahr),
        }
    }
}

impl MonatsName {
    pub fn to_name(self) -> Name {
        Name::new(self.monat)
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct EinnahmenAusgabenAggregation {
    pub einnahmen: Betrag,
    pub ausgaben: Betrag,
}

impl Add for EinnahmenAusgabenAggregation {
    type Output = EinnahmenAusgabenAggregation;

    fn add(self, rhs: Self) -> Self::Output {
        EinnahmenAusgabenAggregation {
            einnahmen: self.einnahmen + rhs.einnahmen,
            ausgaben: self.ausgaben + rhs.ausgaben,
        }
    }
}

impl Default for EinnahmenAusgabenAggregation {
    fn default() -> Self {
        EinnahmenAusgabenAggregation {
            einnahmen: Betrag::new(Vorzeichen::Positiv, 0, 0),
            ausgaben: Betrag::new(Vorzeichen::Negativ, 0, 0),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct KategorieAggregation {
    pub content: HashMap<Kategorie, Betrag>,
}

impl Add for KategorieAggregation {
    type Output = KategorieAggregation;

    fn add(self, rhs: Self) -> Self::Output {
        let mut union: HashMap<Kategorie, Betrag> = self.content.clone();

        for (kategorie, betrag) in rhs.content.iter() {
            let zero = Betrag::zero();
            let current = union.get(&kategorie).unwrap_or(&zero);
            union.insert(kategorie.clone(), current.clone() + betrag.clone());
        }

        KategorieAggregation { content: union }
    }
}

impl Default for KategorieAggregation {
    fn default() -> Self {
        KategorieAggregation {
            content: HashMap::new(),
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::select::functions::datatypes::{
        EinnahmenAusgabenAggregation, MonatsAggregationsIndex,
    };
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use std::cmp::Ordering;

    #[test]
    fn test_monats_aggregation_ord() {
        let a = MonatsAggregationsIndex {
            monat: 1,
            jahr: 2020,
        };
        let b = MonatsAggregationsIndex {
            monat: 2,
            jahr: 2020,
        };

        assert_eq!(a.cmp(&b), Ordering::Less);
        assert_eq!(a.cmp(&a), Ordering::Equal);
        assert_eq!(b.cmp(&a), Ordering::Greater);
    }

    #[test]
    fn test_monats_aggregation_format_descriptive_string() {
        let a = MonatsAggregationsIndex {
            monat: 1,
            jahr: 2020,
        };

        assert_eq!(a.format_descriptive_string().monat, "01/2020".to_string());
    }

    #[test]
    fn test_einnahmen_ausgaben_aggregation_add() {
        let a = EinnahmenAusgabenAggregation {
            einnahmen: Betrag::new(Vorzeichen::Positiv, 1, 0),
            ausgaben: Betrag::new(Vorzeichen::Negativ, 1, 0),
        };
        let b = EinnahmenAusgabenAggregation {
            einnahmen: Betrag::new(Vorzeichen::Positiv, 1, 0),
            ausgaben: Betrag::new(Vorzeichen::Negativ, 1, 0),
        };

        let result = a + b;

        assert_eq!(result.einnahmen, Betrag::new(Vorzeichen::Positiv, 2, 0));
        assert_eq!(result.ausgaben, Betrag::new(Vorzeichen::Negativ, 2, 0));
    }
}
