use crate::budgetbutler::database::change::change::ChangeSelector;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::persistent_state::einzelbuchungen::Einzelbuchungen;

impl ChangeSelector<Einzelbuchung, Einzelbuchungen> {
    pub fn rename_kategorie(
        &self,
        alte_kategorie: Kategorie,
        neue_kategorie: Kategorie,
    ) -> Einzelbuchungen {
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

        Einzelbuchungen {
            einzelbuchungen: neue_buchungen,
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::einzelbuchung::builder::demo_einzelbuchung;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::state::persistent_state::einzelbuchungen::Einzelbuchungen;

    #[test]
    fn test_rename_kategorie() {
        let einzelbuchungen = Einzelbuchungen {
            einzelbuchungen: vec![indiziert(demo_einzelbuchung())],
        };

        let result = einzelbuchungen
            .change()
            .rename_kategorie(demo_kategorie(), kategorie("neue kategorie"));

        assert_eq!(
            result.einzelbuchungen[0].value.kategorie,
            kategorie("neue kategorie")
        );
    }
}
