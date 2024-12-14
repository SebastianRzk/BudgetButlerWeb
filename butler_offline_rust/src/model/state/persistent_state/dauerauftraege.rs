use crate::budgetbutler::database::change::{ChangeSelector, Creates};
use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::dauerauftrag::Dauerauftrag;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::kategorie::Kategorie;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Dauerauftraege {
    pub dauerauftraege: Vec<Indiziert<Dauerauftrag>>,
}

impl Creates<Dauerauftrag, Dauerauftraege> for Dauerauftraege {
    fn create(item: Vec<Indiziert<Dauerauftrag>>) -> Dauerauftraege {
        Dauerauftraege {
            dauerauftraege: item,
        }
    }
}

impl Dauerauftraege {
    pub fn select(&self) -> Selector<Indiziert<Dauerauftrag>> {
        Selector::new(self.dauerauftraege.clone())
    }

    pub fn sort(&self) -> Dauerauftraege {
        let mut neue_buchungen = self.dauerauftraege.clone();
        neue_buchungen.sort();

        Dauerauftraege {
            dauerauftraege: neue_buchungen,
        }
    }

    pub fn get(&self, index: u32) -> Indiziert<Dauerauftrag> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn change(&self) -> ChangeSelector<Dauerauftrag, Dauerauftraege> {
        ChangeSelector {
            content: self.dauerauftraege.clone(),
            output: None,
        }
    }
}

impl ChangeSelector<Dauerauftrag, Dauerauftraege> {
    pub fn rename_kategorie(
        &self,
        alte_kategorie: Kategorie,
        neue_kategorie: Kategorie,
    ) -> Dauerauftraege {
        let neue_buchungen = self
            .content
            .iter()
            .map(|x| {
                if x.value.kategorie == alte_kategorie {
                    Indiziert {
                        value: x.value.clone().change_kategorie(neue_kategorie.clone()),
                        dynamisch: x.dynamisch,
                        index: x.index,
                    }
                } else {
                    x.clone()
                }
            })
            .collect();

        Dauerauftraege {
            dauerauftraege: neue_buchungen,
        }
    }
}