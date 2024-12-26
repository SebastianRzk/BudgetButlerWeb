use crate::budgetbutler::database::change::change::{ChangeSelector, Creates};
use crate::budgetbutler::database::select::functions::keyextractors::kategorie_aggregation;
use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::kategorie::Kategorie;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Einzelbuchungen {
    pub einzelbuchungen: Vec<Indiziert<Einzelbuchung>>,
}

impl Einzelbuchungen {
    pub fn select(&self) -> Selector<Indiziert<Einzelbuchung>> {
        Selector::new(self.einzelbuchungen.clone())
    }

    pub fn get(&self, index: u32) -> Indiziert<Einzelbuchung> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn change(&self) -> ChangeSelector<Einzelbuchung, Einzelbuchungen> {
        ChangeSelector {
            content: self.einzelbuchungen.clone(),
            output: None,
        }
    }

    pub fn sort(&self) -> Einzelbuchungen {
        let mut neue_buchungen = self.einzelbuchungen.clone();
        neue_buchungen.sort();

        Einzelbuchungen {
            einzelbuchungen: neue_buchungen,
        }
    }

    pub fn get_kategorien(&self) -> Vec<Kategorie> {
        self.select().extract_unique_values(kategorie_aggregation)
    }
}

impl Creates<Einzelbuchung, Einzelbuchungen> for Einzelbuchungen {
    fn create(item: Vec<Indiziert<Einzelbuchung>>) -> Einzelbuchungen {
        Einzelbuchungen {
            einzelbuchungen: item,
        }
    }
}
