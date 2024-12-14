use crate::budgetbutler::database::change::{ChangeSelector, Creates};
use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::person::Person;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct GemeinsameBuchungen {
    pub gemeinsame_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
}

impl Creates<GemeinsameBuchung, GemeinsameBuchungen> for GemeinsameBuchungen {
    fn create(item: Vec<Indiziert<GemeinsameBuchung>>) -> GemeinsameBuchungen {
        GemeinsameBuchungen {
            gemeinsame_buchungen: item,
        }
    }
}

impl GemeinsameBuchungen {
    pub fn sort(&self) -> GemeinsameBuchungen {
        let mut neue_buchungen = self.gemeinsame_buchungen.clone();
        neue_buchungen.sort();

        GemeinsameBuchungen {
            gemeinsame_buchungen: neue_buchungen,
        }
    }

    pub fn get(&self, index: u32) -> Indiziert<GemeinsameBuchung> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn select(&self) -> Selector<Indiziert<GemeinsameBuchung>> {
        Selector::new(self.gemeinsame_buchungen.clone())
    }

    pub fn change(&self) -> ChangeSelector<GemeinsameBuchung, GemeinsameBuchungen> {
        ChangeSelector {
            content: self.gemeinsame_buchungen.clone(),
            output: None,
        }
    }
}

impl ChangeSelector<GemeinsameBuchung, GemeinsameBuchungen> {
    pub fn rename_person(&self, alter_name: Person, neuer_name: Person) -> GemeinsameBuchungen {
        let neue_buchungen = self
            .content
            .iter()
            .map(|x| {
                if x.value.person == alter_name {
                    Indiziert {
                        value: x.value.clone().change_person(neuer_name.clone()),
                        dynamisch: x.dynamisch,
                        index: x.index,
                    }
                } else {
                    x.clone()
                }
            })
            .collect();

        GemeinsameBuchungen {
            gemeinsame_buchungen: neue_buchungen,
        }
    }

    pub fn rename_kategorie(
        &self,
        alte_kategorie: Kategorie,
        neue_kategorie: Kategorie,
    ) -> GemeinsameBuchungen {
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

        GemeinsameBuchungen {
            gemeinsame_buchungen: neue_buchungen,
        }
    }
}