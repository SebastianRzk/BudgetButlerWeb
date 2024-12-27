use crate::io::html::input::select::Select;
use crate::model::primitives::kategorie::Kategorie;

pub fn flatmap_kategorien(kategorien: Vec<Kategorie>) -> Vec<String> {
    kategorien.iter().map(|x| x.kategorie.clone()).collect()
}

pub fn flatmap_kategorien_option(
    kategorien: Vec<Kategorie>,
    selected: Kategorie,
) -> Select<String> {
    Select::new(
        flatmap_kategorien(kategorien),
        Some(selected.kategorie.clone()),
    )
}

#[cfg(test)]
mod tests {
    use crate::model::primitives::kategorie::Kategorie;

    #[test]
    fn test_flatmap_kategorien() {
        let kategorien = vec![
            Kategorie::new("test1".to_string()),
            Kategorie::new("test2".to_string()),
        ];

        let result = super::flatmap_kategorien(kategorien);

        assert_eq!(result, vec!["test1".to_string(), "test2".to_string()]);
    }

    #[test]
    fn test_flatmap_kategorien_option() {
        let kategorien = vec![
            Kategorie::new("test1".to_string()),
            Kategorie::new("test2".to_string()),
        ];

        let selected = Kategorie::new("test2".to_string());

        let result = super::flatmap_kategorien_option(kategorien, selected);

        assert_eq!(result.items.len(), 2);
        assert_eq!(result.items[0].value, "test1");
        assert_eq!(result.items[0].selected, false);
        assert_eq!(result.items[1].value, "test2");
        assert_eq!(result.items[1].selected, true);
    }
}
