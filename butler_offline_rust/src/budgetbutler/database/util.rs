use crate::budgetbutler::database::select::functions::keyextractors::kategorie_aggregation;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::persistent_application_state::Einzelbuchungen;

pub fn calc_kategorien(einzelbuchungen: &Einzelbuchungen, extra_kategorie: &Option<Kategorie>) -> Vec<Kategorie> {
    let mut kategorien = einzelbuchungen.select().extract_unique_values(kategorie_aggregation);
    if let Some(extra_kategorie) = extra_kategorie {
        kategorien.push(extra_kategorie.clone());
    }
    kategorien.sort();
    kategorien
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::util::calc_kategorien;
    use crate::model::einzelbuchung::builder::to_einzelbuchung_with_kategorie;
    use crate::model::primitives::kategorie::Kategorie;
    use crate::model::state::persistent_application_state::builder::generate_database_with_einzelbuchungen;

    #[test]
    pub fn test_calc_kategorien() {
        let database = generate_database_with_einzelbuchungen(vec![
            to_einzelbuchung_with_kategorie("test_kategorie")]);
        let kategorien = calc_kategorien(&database.einzelbuchungen, &None);

        assert_eq!(kategorien.len(), 1);
        assert_eq!(kategorien[0].get_kategorie(), "test_kategorie");
    }

    #[test]
    pub fn test_calc_kategorien_with_extra_kategorie() {
        let database = generate_database_with_einzelbuchungen(vec![
            to_einzelbuchung_with_kategorie("test_kategorie")
        ]);
        let kategorien = calc_kategorien(&database.einzelbuchungen, &Some(Kategorie::new("extra_kategorie".to_string())));
        assert_eq!(kategorien.len(), 2);
        assert_eq!(kategorien[0].get_kategorie(), "extra_kategorie");
        assert_eq!(kategorien[1].get_kategorie(), "test_kategorie");
    }
}