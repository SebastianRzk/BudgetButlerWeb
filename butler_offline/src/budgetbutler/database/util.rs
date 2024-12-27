use crate::budgetbutler::database::select::functions::keyextractors::kategorie_aggregation;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::persistent_state::einzelbuchungen::Einzelbuchungen;

pub fn calc_kategorien(
    einzelbuchungen: &Einzelbuchungen,
    extra_kategorie: &Option<Kategorie>,
    ausgeschlossene_kategorien: &Vec<Kategorie>,
) -> Vec<Kategorie> {
    let mut kategorien = einzelbuchungen
        .select()
        .extract_unique_values(kategorie_aggregation);
    if let Some(extra_kategorie) = extra_kategorie {
        if !kategorien.contains(extra_kategorie) {
            kategorien.push(extra_kategorie.clone());
        }
    }
    for kategorie in ausgeschlossene_kategorien {
        kategorien.retain(|x| x != kategorie);
    }
    kategorien.sort();
    kategorien
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::util::calc_kategorien;
    use crate::model::database::einzelbuchung::builder::einzelbuchung_with_kategorie;
    use crate::model::primitives::kategorie::{kategorie, Kategorie};
    use crate::model::state::persistent_application_state::builder::generate_database_with_einzelbuchungen;

    #[test]
    pub fn test_calc_kategorien() {
        let database = generate_database_with_einzelbuchungen(vec![einzelbuchung_with_kategorie(
            "test_kategorie",
        )]);
        let kategorien = calc_kategorien(&database.einzelbuchungen, &None, &vec![]);

        assert_eq!(kategorien.len(), 1);
        assert_eq!(kategorien[0].get_kategorie(), "test_kategorie");
    }

    #[test]
    pub fn test_calc_kategorien_with_extra_kategorie() {
        let database = generate_database_with_einzelbuchungen(vec![einzelbuchung_with_kategorie(
            "test_kategorie",
        )]);
        let kategorien = calc_kategorien(
            &database.einzelbuchungen,
            &Some(Kategorie::new("extra_kategorie".to_string())),
            &vec![],
        );
        assert_eq!(kategorien.len(), 2);
        assert_eq!(kategorien[0].get_kategorie(), "extra_kategorie");
        assert_eq!(kategorien[1].get_kategorie(), "test_kategorie");
    }

    #[test]
    pub fn test_calc_kategorien_should_filter_doppelte() {
        let database = generate_database_with_einzelbuchungen(vec![einzelbuchung_with_kategorie(
            "test_kategorie",
        )]);
        let kategorien = calc_kategorien(
            &database.einzelbuchungen,
            &Some(kategorie("test_kategorie")),
            &vec![],
        );
        assert_eq!(kategorien.len(), 1);
        assert_eq!(kategorien[0].get_kategorie(), "test_kategorie");
    }

    #[test]
    pub fn test_should_filter_ausgeschlossene() {
        let database = generate_database_with_einzelbuchungen(vec![
            einzelbuchung_with_kategorie("test_kategorie"),
            einzelbuchung_with_kategorie("test_kategorie2"),
        ]);
        let kategorien = calc_kategorien(
            &database.einzelbuchungen,
            &None,
            &vec![kategorie("test_kategorie2")],
        );
        assert_eq!(kategorien.len(), 1);
        assert_eq!(kategorien[0].get_kategorie(), "test_kategorie");
    }
}
