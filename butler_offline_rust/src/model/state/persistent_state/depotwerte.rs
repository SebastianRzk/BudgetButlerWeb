use crate::budgetbutler::database::change::{ChangeSelector, Creates};
use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::depotwert::Depotwert;
use crate::model::indiziert::Indiziert;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Depotwerte {
    pub depotwerte: Vec<Indiziert<Depotwert>>,
}

impl Creates<Depotwert, Depotwerte> for Depotwerte {
    fn create(item: Vec<Indiziert<Depotwert>>) -> Depotwerte {
        Depotwerte { depotwerte: item }
    }
}

impl Depotwerte {
    pub fn select(&self) -> Selector<Indiziert<Depotwert>> {
        Selector::new(self.depotwerte.clone())
    }

    pub fn sort(&self) -> Depotwerte {
        let mut neue_depotwerte = self.depotwerte.clone();
        neue_depotwerte.sort();

        Depotwerte {
            depotwerte: neue_depotwerte,
        }
    }

    pub fn get(&self, index: u32) -> Indiziert<Depotwert> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn change(&self) -> ChangeSelector<Depotwert, Depotwerte> {
        ChangeSelector {
            content: self.depotwerte.clone(),
            output: None,
        }
    }
}
