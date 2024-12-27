use crate::model::primitives::type_description::TypeDescription;

pub struct Select<T> {
    pub items: Vec<SelectItem<T>>,
}

pub struct SelectItem<T> {
    pub value: T,
    pub selected: bool,
}

impl<T: PartialEq> Select<T> {
    pub fn new(items: Vec<T>, selected: Option<T>) -> Select<T> {
        Select {
            items: items
                .into_iter()
                .map(|item| SelectItem {
                    selected: selected.as_ref().map_or(false, |x: &T| x.eq(&item)),
                    value: item,
                })
                .collect(),
        }
    }
}

pub fn new_select_with_description(
    items: Vec<TypeDescription<String>>,
    selected_value: Option<String>,
) -> Select<DescriptiveSelectItem> {
    Select {
        items: items
            .into_iter()
            .map(|item| SelectItem {
                selected: selected_value
                    .as_ref()
                    .map_or(false, |x: &String| x.eq(&item.value)),
                value: DescriptiveSelectItem {
                    value: item.value,
                    description: item.description,
                },
            })
            .collect(),
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DescriptiveSelectItem {
    pub value: String,
    pub description: String,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_select_new() {
        let items = vec![1, 2, 3];
        let selected = Some(2);
        let select = Select::new(items, selected);
        assert_eq!(select.items.len(), 3);
        assert_eq!(select.items[0].selected, false);
        assert_eq!(select.items[1].selected, true);
        assert_eq!(select.items[2].selected, false);
    }

    #[test]
    fn test_select_with_description() {
        let select = new_select_with_description(
            vec![
                TypeDescription {
                    value: "1".to_string(),
                    description: "one".to_string(),
                },
                TypeDescription {
                    value: "2".to_string(),
                    description: "two".to_string(),
                },
            ],
            Some("2".to_string()),
        );

        assert_eq!(select.items.len(), 2);
        assert_eq!(select.items[0].selected, false);
        assert_eq!(select.items[1].selected, true);
    }
}
