use crate::budgetbutler::database::change::change::{ChangeSelector, Creates};
use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::depotauszug::Depotauszug;
use crate::model::indiziert::Indiziert;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Depotauszuege {
    pub depotauszuege: Vec<Indiziert<Depotauszug>>,
}

impl Creates<Depotauszug, Depotauszuege> for Depotauszuege {
    fn create(item: Vec<Indiziert<Depotauszug>>) -> Depotauszuege {
        Depotauszuege {
            depotauszuege: item,
        }
    }
}

impl Depotauszuege {
    pub fn select(&self) -> Selector<Indiziert<Depotauszug>> {
        Selector::new(self.depotauszuege.clone())
    }

    pub fn sort(&self) -> Depotauszuege {
        let mut neue_auszuege = self.depotauszuege.clone();
        neue_auszuege.sort();

        Depotauszuege {
            depotauszuege: neue_auszuege,
        }
    }

    pub fn get(&self, index: u32) -> Indiziert<Depotauszug> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn change(&self) -> ChangeSelector<Depotauszug, Depotauszuege> {
        ChangeSelector {
            content: self.depotauszuege.clone(),
            output: None,
        }
    }
}
