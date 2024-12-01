use crate::model::eigenschaften::besitzt_start_und_ende_datum::BesitztStartUndEndeDatum;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::rhythmus::Rhythmus;
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Dauerauftrag {
    pub start_datum: Datum,
    pub ende_datum: Datum,
    pub name: Name,
    pub kategorie: Kategorie,
    pub betrag: Betrag,
    pub rhythmus: Rhythmus,
}

impl PartialOrd<Self> for Dauerauftrag {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Dauerauftrag {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        let ordering = self.start_datum.cmp(&other.start_datum);
        if ordering == Ordering::Equal {
            self.name.cmp(&other.name)
        } else {
            ordering
        }
    }
}

impl<'a> BesitztStartUndEndeDatum<'a> for Indiziert<Dauerauftrag> {
    fn start_datum(&self) -> &Datum {
        &self.value.start_datum
    }

    fn ende_datum(&self) -> &Datum {
        &self.value.ende_datum
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::dauerauftrag::Dauerauftrag;
    use crate::model::primitives::betrag::builder::any_betrag;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::builder::any_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::builder::any_name;
    use crate::model::primitives::rhythmus::Rhythmus;

    pub fn dauerauftrag_mit_start_ende_datum(start_datum: Datum, ende_datum: Datum) -> Dauerauftrag {
        Dauerauftrag {
            start_datum,
            ende_datum,
            name: any_name(),
            kategorie: any_kategorie(),
            betrag: any_betrag(),
            rhythmus: Rhythmus::Halbjaehrlich,
        }
    }

    pub fn dauerauftrag_mit_kategorie(k: &str) -> Dauerauftrag {
        Dauerauftrag {
            start_datum: any_datum(),
            ende_datum: any_datum(),
            name: any_name(),
            kategorie: kategorie(k),
            betrag: any_betrag(),
            rhythmus: Rhythmus::Halbjaehrlich,
        }
    }

    pub fn any_dauerauftrag() -> Dauerauftrag {
        Dauerauftrag {
            start_datum: any_datum(),
            ende_datum: any_datum(),
            name: any_name(),
            kategorie: any_kategorie(),
            betrag: any_betrag(),
            rhythmus: Rhythmus::Halbjaehrlich,
        }
    }
}


#[cfg(test)]
mod test {}