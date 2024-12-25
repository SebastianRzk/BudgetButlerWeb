use crate::budgetbutler::database::change::change::ChangeSelector;
use crate::model::database::dauerauftrag::Dauerauftrag;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::persistent_state::dauerauftraege::Dauerauftraege;

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

#[cfg(test)]
mod tests {
    use crate::model::database::dauerauftrag::builder::demo_dauerauftrag;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::state::persistent_state::dauerauftraege::Dauerauftraege;

    #[test]
    fn test_rename_kategorie() {
        let dauerauftraege = Dauerauftraege {
            dauerauftraege: vec![indiziert(demo_dauerauftrag())],
        };

        let result = dauerauftraege
            .change()
            .rename_kategorie(demo_kategorie(), kategorie("neue kategorie"));

        assert_eq!(
            result.dauerauftraege[0].value.kategorie,
            kategorie("neue kategorie")
        );
    }
}
