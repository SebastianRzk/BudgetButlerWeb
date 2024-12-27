use crate::budgetbutler::database::change::change::{ChangeSelector, Creates};
use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::sparbuchung::Sparbuchung;
use crate::model::indiziert::Indiziert;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Sparbuchungen {
    pub sparbuchungen: Vec<Indiziert<Sparbuchung>>,
}

impl Creates<Sparbuchung, Sparbuchungen> for Sparbuchungen {
    fn create(item: Vec<Indiziert<Sparbuchung>>) -> Sparbuchungen {
        Sparbuchungen {
            sparbuchungen: item,
        }
    }
}

impl Sparbuchungen {
    pub fn select(&self) -> Selector<Indiziert<Sparbuchung>> {
        Selector::new(self.sparbuchungen.clone())
    }

    pub fn sort(&self) -> Sparbuchungen {
        let mut neue_sparbuchungen = self.sparbuchungen.clone();
        neue_sparbuchungen.sort();

        Sparbuchungen {
            sparbuchungen: neue_sparbuchungen,
        }
    }

    pub fn get(&self, index: u32) -> Indiziert<Sparbuchung> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn change(&self) -> ChangeSelector<Sparbuchung, Sparbuchungen> {
        ChangeSelector {
            content: self.sparbuchungen.clone(),
            output: None,
        }
    }
}
