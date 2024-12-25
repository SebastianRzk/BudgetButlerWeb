use crate::io::disk::database::types::ElementRequirement;
use crate::model::indiziert::Indiziert;

pub fn index_dynamic<T: ElementRequirement>(
    items: Vec<T>,
    current_index: u32,
) -> DynamicIndexResult<T> {
    let mut new_index = current_index + 1;
    let values = items
        .into_iter()
        .map(|item| {
            let indiziert = Indiziert {
                index: new_index,
                dynamisch: true,
                value: item,
            };
            new_index += 1;
            indiziert
        })
        .collect();

    DynamicIndexResult { new_index, values }
}

pub struct DynamicIndexResult<T: ElementRequirement> {
    pub new_index: u32,
    pub values: Vec<Indiziert<T>>,
}

#[cfg(test)]
mod tests {
    use super::*;

    impl ElementRequirement for i32 {}

    #[test]
    fn test_index_dynamic() {
        let items = vec![1, 2, 3];
        let current_index = 0;
        let result = index_dynamic(items, current_index);
        assert_eq!(result.new_index, 4);
        assert_eq!(result.values.len(), 3);
        assert_eq!(result.values[0].index, 1);
        assert_eq!(result.values[1].index, 2);
        assert_eq!(result.values[2].index, 3);
        assert_eq!(result.values[0].dynamisch, true);
        assert_eq!(result.values[1].dynamisch, true);
        assert_eq!(result.values[2].dynamisch, true);
    }
}
