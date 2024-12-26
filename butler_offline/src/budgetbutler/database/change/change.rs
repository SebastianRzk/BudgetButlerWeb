use crate::model::indiziert::Indiziert;

pub struct ChangeSelector<T: PartialEq + Eq + Ord + PartialOrd, K> {
    pub content: Vec<Indiziert<T>>,
    //TODO: Figure out, whats right here
    pub output: Option<K>,
}

pub trait Creates<T: PartialEq + Eq + Ord + PartialOrd + Clone, K> {
    fn create(item: Vec<Indiziert<T>>) -> K;
}

impl<T: PartialEq + Eq + Ord + PartialOrd + Clone, K: Creates<T, K>> ChangeSelector<T, K> {
    pub fn edit(&self, index: u32, new_item: T) -> K {
        let mut neue_buchungen = self.content.clone();
        for buchung in neue_buchungen.iter_mut() {
            if buchung.index == index {
                buchung.value = new_item.clone();
            }
        }
        K::create(neue_buchungen)
    }

    pub fn insert(&self, item: T) -> K {
        let mut neue_buchungen = self.content.clone();
        neue_buchungen.push(Indiziert {
            value: item,
            dynamisch: false,
            index: 0,
        });
        K::create(neue_buchungen)
    }

    pub fn insert_all(&self, item: Vec<T>) -> K {
        let mut neue_buchungen = self.content.clone();
        for buchung in item.iter() {
            neue_buchungen.push(Indiziert {
                value: buchung.clone(),
                dynamisch: false,
                index: 0,
            });
        }
        K::create(neue_buchungen)
    }

    pub fn delete(&self, index: u32) -> K {
        let mut neue_buchungen = self.content.clone();
        neue_buchungen.retain(|buchung| buchung.index != index);

        K::create(neue_buchungen)
    }

    pub fn delete_all(&self, index: Vec<u32>) -> K {
        let mut neue_buchungen = self.content.clone();
        neue_buchungen.retain(|buchung| !index.contains(&buchung.index));

        K::create(neue_buchungen)
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::dauerauftrag::builder::dauerauftrag_mit_kategorie;
    use crate::model::database::einzelbuchung::builder::einzelbuchung_with_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::state::persistent_application_state::builder::{
        dauerauftrage, einzelbuchungen,
    };
    use crate::model::state::persistent_state::dauerauftraege::Dauerauftraege;
    use crate::model::state::persistent_state::einzelbuchungen::Einzelbuchungen;

    #[test]
    fn test_einzelbuchungen_edit() {
        let einzelbuchungen = einzelbuchungen(einzelbuchung_with_kategorie("test_kategorie"));

        let result = einzelbuchungen
            .change()
            .edit(0, einzelbuchung_with_kategorie("edited_kategorie"));

        assert_eq!(result.get(0).value.kategorie, kategorie("edited_kategorie"));
    }
    #[test]
    fn test_dauerauftraege_edit() {
        let einzelbuchungen = dauerauftrage(dauerauftrag_mit_kategorie("test_kategorie"));

        let result = einzelbuchungen
            .change()
            .edit(0, dauerauftrag_mit_kategorie("edited_kategorie"));

        assert_eq!(result.get(0).value.kategorie, kategorie("edited_kategorie"));
    }

    #[test]
    fn test_dauerauftraege_add() {
        let dauerauftraege = dauerauftrage(dauerauftrag_mit_kategorie("test_kategorie"));
        let result = dauerauftraege
            .change()
            .insert(dauerauftrag_mit_kategorie("test_kategorie"));
        assert_eq!(result.select().count(), 2);
    }

    #[test]
    fn test_einzelbuchungen_add() {
        let einzelbuchungen = einzelbuchungen(einzelbuchung_with_kategorie("test_kategorie"));
        let result = einzelbuchungen
            .change()
            .insert(einzelbuchung_with_kategorie("test_kategorie"));
        assert_eq!(result.select().count(), 2);
    }

    #[test]
    fn test_delete_einzelbuchung() {
        let einzelbuchungen = Einzelbuchungen {
            einzelbuchungen: vec![
                super::Indiziert {
                    value: einzelbuchung_with_kategorie("to delete"),
                    dynamisch: false,
                    index: 0,
                },
                super::Indiziert {
                    value: einzelbuchung_with_kategorie("to retain"),
                    dynamisch: false,
                    index: 1,
                },
            ],
        };

        let result = einzelbuchungen.change().delete(0);

        assert_eq!(result.select().count(), 1);
        assert_eq!(result.get(1).value.kategorie, kategorie("to retain"));
    }

    #[test]
    fn test_delete_dauerauftraege() {
        let einzelbuchungen = Dauerauftraege {
            dauerauftraege: vec![
                super::Indiziert {
                    value: dauerauftrag_mit_kategorie("to delete"),
                    dynamisch: false,
                    index: 0,
                },
                super::Indiziert {
                    value: dauerauftrag_mit_kategorie("to retain"),
                    dynamisch: false,
                    index: 1,
                },
            ],
        };

        let result = einzelbuchungen.change().delete(0);

        assert_eq!(result.select().count(), 1);
        assert_eq!(result.get(1).value.kategorie, kategorie("to retain"));
    }
}
