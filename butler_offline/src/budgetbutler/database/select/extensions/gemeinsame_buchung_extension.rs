use crate::budgetbutler::database::change::change::ChangeSelector;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::person::Person;
use crate::model::state::persistent_state::gemeinsame_buchungen::GemeinsameBuchungen;

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

#[cfg(test)]
mod tests {
    use crate::model::database::gemeinsame_buchung::builder::demo_gemeinsame_buchung;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::person::builder::{demo_person, person};
    use crate::model::state::persistent_state::gemeinsame_buchungen::GemeinsameBuchungen;

    #[test]
    fn test_rename_person() {
        let gemeinsame_buchungen = GemeinsameBuchungen {
            gemeinsame_buchungen: vec![indiziert(demo_gemeinsame_buchung())],
        };

        let result = gemeinsame_buchungen
            .change()
            .rename_person(demo_person(), person("neuer name"));

        assert_eq!(
            result.gemeinsame_buchungen[0].value.person,
            person("neuer name")
        );
    }

    #[test]
    fn test_rename_kategorie() {
        let gemeinsame_buchungen = GemeinsameBuchungen {
            gemeinsame_buchungen: vec![indiziert(demo_gemeinsame_buchung())],
        };

        let result = gemeinsame_buchungen
            .change()
            .rename_kategorie(demo_kategorie(), kategorie("neue kategorie"));

        assert_eq!(
            result.gemeinsame_buchungen[0].value.kategorie,
            kategorie("neue kategorie")
        );
    }
}
