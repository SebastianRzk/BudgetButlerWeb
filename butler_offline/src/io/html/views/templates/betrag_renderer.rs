use crate::model::primitives::betrag::Betrag;

impl Betrag {
    pub fn to_input_string(&self) -> String {
        if self.as_cent() == 0 {
            return "".to_string();
        }
        self.to_german_string()
    }
}

#[cfg(test)]
mod tests {
    use crate::model::primitives::betrag::Vorzeichen;

    #[test]
    fn test_with_zero_should_return_empty_string() {
        let betrag = crate::model::primitives::betrag::Betrag::zero();
        let result = betrag.to_input_string();
        assert_eq!(result, "".to_string());
    }

    #[test]
    fn test_with_non_zero_should_return_string() {
        let betrag = crate::model::primitives::betrag::Betrag::from_cent(Vorzeichen::Positiv, 100);
        let result = betrag.to_input_string();
        assert_eq!(result, "1,00".to_string());
    }
}
