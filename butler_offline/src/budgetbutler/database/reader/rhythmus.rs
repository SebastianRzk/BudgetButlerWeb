use crate::model::primitives::rhythmus::Rhythmus;

pub fn get_monatsdelta_for_rhythmus(rhythmus: Rhythmus) -> u32 {
    match rhythmus {
        Rhythmus::Monatlich => 1,
        Rhythmus::Vierteljaehrlich => 3,
        Rhythmus::Halbjaehrlich => 6,
        Rhythmus::Jaehrlich => 12,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::primitives::rhythmus::Rhythmus;

    #[test]
    fn test_get_monatsdelta_for_rhythmus() {
        assert_eq!(get_monatsdelta_for_rhythmus(Rhythmus::Monatlich), 1);
        assert_eq!(get_monatsdelta_for_rhythmus(Rhythmus::Vierteljaehrlich), 3);
        assert_eq!(get_monatsdelta_for_rhythmus(Rhythmus::Halbjaehrlich), 6);
        assert_eq!(get_monatsdelta_for_rhythmus(Rhythmus::Jaehrlich), 12);
    }
}
