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
            items: items.into_iter().map(|item| {
                SelectItem {
                    selected: selected.as_ref().map_or(false, |x: &T| x.eq(&item)),
                    value: item,
                }
            }).collect()
        }
    }
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
}