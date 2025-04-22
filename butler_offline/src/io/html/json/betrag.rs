use crate::model::primitives::betrag::Betrag;
use std::fmt::Display;

impl Display for Betrag {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}{}.{:02}", self.vorzeichen, self.euro, self.cent)
    }
}

#[cfg(test)]
mod tests {
    use crate::io::html::json::list::JSONBetragList;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};

    #[test]
    fn test_json_betrag_list() {
        let betrag_list = JSONBetragList::new(vec![
            Betrag::new(Vorzeichen::Positiv, 10, 10),
            Betrag::new(Vorzeichen::Negativ, 20, 20),
        ]);
        assert_eq!(betrag_list.to_string(), "[\"10.10\",\"-20.20\"]");
    }

    #[test]
    fn test_should_format_nachkommastelle_korrekt() {
        let betrag = Betrag::new(Vorzeichen::Positiv, 0, 1);
        assert_eq!(betrag.to_string(), "0.01");
    }
}
