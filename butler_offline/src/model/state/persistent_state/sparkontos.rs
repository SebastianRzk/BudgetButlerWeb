use crate::budgetbutler::database::change::change::{ChangeSelector, Creates};
use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::sparkonto::Sparkonto;
use crate::model::indiziert::Indiziert;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Sparkontos {
    pub sparkontos: Vec<Indiziert<Sparkonto>>,
}

impl Creates<Sparkonto, Sparkontos> for Sparkontos {
    fn create(item: Vec<Indiziert<Sparkonto>>) -> Sparkontos {
        Sparkontos { sparkontos: item }
    }
}

impl Sparkontos {
    pub fn select(&self) -> Selector<Indiziert<Sparkonto>> {
        Selector::new(self.sparkontos.clone())
    }

    pub fn sort(&self) -> Sparkontos {
        let mut neue_kontos = self.sparkontos.clone();
        neue_kontos.sort();

        Sparkontos {
            sparkontos: neue_kontos,
        }
    }

    pub fn get(&self, index: u32) -> Indiziert<Sparkonto> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn change(&self) -> ChangeSelector<Sparkonto, Sparkontos> {
        ChangeSelector {
            content: self.sparkontos.clone(),
            output: None,
        }
    }
}
