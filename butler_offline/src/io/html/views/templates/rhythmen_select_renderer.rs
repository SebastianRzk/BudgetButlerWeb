use crate::io::disk::primitive::rhythmus::write_rhythmus;
use crate::io::html::input::select::Select;
use crate::model::primitives::rhythmus::Rhythmus;

pub fn create_rhythmen_select(
    selected_rhythmus: Rhythmus,
    alle_rhythmen: Vec<Rhythmus>,
) -> Select<String> {
    Select::new(
        alle_rhythmen
            .iter()
            .map(|x| write_rhythmus(x.clone()).element)
            .collect(),
        Some(write_rhythmus(selected_rhythmus).element),
    )
}

#[cfg(test)]
mod tests {
    use crate::io::html::views::templates::rhythmen_select_renderer::create_rhythmen_select;
    use crate::model::primitives::rhythmus::Rhythmus;

    #[test]
    fn test_create_rhythmen_select() {
        let selected_rhythmus = Rhythmus::Monatlich;
        let alle_rhythmen = vec![Rhythmus::Monatlich, Rhythmus::Vierteljaehrlich];
        let result = create_rhythmen_select(selected_rhythmus, alle_rhythmen);

        assert_eq!(result.items.len(), 2);
        assert_eq!(result.items[0].value, "monatlich");
        assert_eq!(result.items[0].selected, true);
        assert_eq!(result.items[1].value, "vierteljährlich");
        assert_eq!(result.items[1].selected, false);
    }
}
