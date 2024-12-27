use crate::model::primitives::betrag::{parse_number, parse_number_str, Betrag, Vorzeichen};

#[derive(Debug, Clone, Eq, PartialEq)]
pub struct BetragOhneVorzeichen {
    pub euro: u32,
    pub cent: u8,
}

impl BetragOhneVorzeichen {
    pub fn new(euro: u32, cent: u8) -> BetragOhneVorzeichen {
        BetragOhneVorzeichen { euro, cent }
    }

    pub fn negativ(&self) -> Betrag {
        Betrag::new(Vorzeichen::Negativ, self.euro, self.cent)
    }

    pub fn positiv(&self) -> Betrag {
        Betrag::new(Vorzeichen::Positiv, self.euro, self.cent)
    }

    pub fn from_iso_string(string_to_parse: &String) -> BetragOhneVorzeichen {
        if !string_to_parse.contains('.') {
            return BetragOhneVorzeichen::new(parse_number(string_to_parse.clone()), 0);
        }
        let mut slitted = string_to_parse.split('.');
        let euro_as_string = slitted.next().unwrap();
        let cent_as_string = slitted.next().unwrap();
        BetragOhneVorzeichen::new(
            parse_number_str(euro_as_string),
            parse_number_str(cent_as_string) as u8,
        )
    }

    pub fn from_user_input(user_input_string: &String) -> BetragOhneVorzeichen {
        BetragOhneVorzeichen::from_iso_string(&user_input_string.replace(",", "."))
    }

    pub fn to_input_string(&self) -> String {
        if self == &BetragOhneVorzeichen::zero() {
            return "".to_string();
        }
        self.to_german_string()
    }

    pub fn to_german_string(&self) -> String {
        format!("{},{:02}", self.euro, self.cent)
    }

    pub fn to_iso_string(&self) -> String {
        format!("{}.{:02}", self.euro, self.cent)
    }

    pub fn zero() -> BetragOhneVorzeichen {
        BetragOhneVorzeichen::new(0, 0)
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;

    pub fn any_betrag() -> BetragOhneVorzeichen {
        BetragOhneVorzeichen::new(10, 10)
    }

    pub fn u_zwei() -> BetragOhneVorzeichen {
        BetragOhneVorzeichen::new(2, 0)
    }

    pub fn u_vier() -> BetragOhneVorzeichen {
        BetragOhneVorzeichen::new(4, 0)
    }

    pub fn u_fuenf() -> BetragOhneVorzeichen {
        BetragOhneVorzeichen::new(5, 0)
    }

    pub fn zero() -> BetragOhneVorzeichen {
        BetragOhneVorzeichen::new(0, 0)
    }
}

#[cfg(test)]
mod tests_betrag_ohne_vorzeichen {
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;

    #[test]
    fn test_positiv() {
        let betrag = BetragOhneVorzeichen { euro: 100, cent: 0 };
        assert_eq!(betrag.positiv(), Betrag::new(Vorzeichen::Positiv, 100, 0));
    }

    #[test]
    fn test_negativ() {
        let betrag = BetragOhneVorzeichen { euro: 100, cent: 0 };
        assert_eq!(betrag.negativ(), Betrag::new(Vorzeichen::Negativ, 100, 0));
    }

    #[test]
    fn test_from_iso_string() {
        assert_eq!(
            BetragOhneVorzeichen::from_iso_string(&"100.1".to_string()),
            BetragOhneVorzeichen { euro: 100, cent: 1 }
        );
        assert_eq!(
            BetragOhneVorzeichen::from_iso_string(&"100".to_string()),
            BetragOhneVorzeichen { euro: 100, cent: 0 }
        );
    }

    #[test]
    fn test_from_input_string() {
        assert_eq!(
            BetragOhneVorzeichen::from_user_input(&"10,11".to_string()),
            BetragOhneVorzeichen { euro: 10, cent: 11 }
        )
    }

    #[test]
    fn test_to_iso_string() {
        assert_eq!(
            BetragOhneVorzeichen { euro: 100, cent: 1 }.to_iso_string(),
            "100.01".to_string()
        );
        assert_eq!(
            BetragOhneVorzeichen { euro: 100, cent: 0 }.to_iso_string(),
            "100.00".to_string()
        );
    }

    #[test]
    fn test_to_german_string() {
        assert_eq!(
            BetragOhneVorzeichen { euro: 100, cent: 1 }.to_german_string(),
            "100,01".to_string()
        );
        assert_eq!(
            BetragOhneVorzeichen { euro: 100, cent: 0 }.to_german_string(),
            "100,00".to_string()
        );
    }

    #[test]
    fn test_to_input_string() {
        assert_eq!(
            BetragOhneVorzeichen::zero().to_input_string(),
            "".to_string()
        );
        assert_eq!(
            BetragOhneVorzeichen { euro: 100, cent: 1 }.to_input_string(),
            "100,01".to_string()
        );
        assert_eq!(
            BetragOhneVorzeichen { euro: 100, cent: 0 }.to_input_string(),
            "100,00".to_string()
        );
    }

    #[test]
    fn test_zero() {
        assert_eq!(
            BetragOhneVorzeichen::zero(),
            BetragOhneVorzeichen { euro: 0, cent: 0 }
        );
    }
}
