use crate::model::primitives::betrag::Betrag;
use std::fmt::Display;

pub struct JSONBetragList {
    content: Vec<Betrag>,
}

impl Display for JSONBetragList {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let content = self
            .content
            .iter()
            .map(|element| {
                let format = format!("\"{}\"", element);
                format
            })
            .collect::<Vec<String>>()
            .join(",");
        write!(f, "{}", format!("[{}]", content))
    }
}

impl JSONBetragList {
    pub fn new(content: Vec<Betrag>) -> JSONBetragList {
        JSONBetragList { content }
    }
}

pub struct JSONStringList {
    content: Vec<String>,
}

impl Display for JSONStringList {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let content = self
            .content
            .iter()
            .map(|element| format!("\"{}\"", element))
            .collect::<Vec<String>>()
            .join(",");
        write!(f, "{}", format!("[{}]", content))
    }
}

impl JSONStringList {
    pub fn new(content: Vec<String>) -> JSONStringList {
        JSONStringList { content }
    }
}

#[cfg(test)]
pub mod tests {
    use crate::io::html::json::list::{JSONBetragList, JSONStringList};
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
    fn test_json_string_list() {
        let string_list = JSONStringList::new(vec![
            "jan".to_string(),
            "feb".to_string(),
            "mar".to_string(),
        ]);
        assert_eq!(string_list.to_string(), "[\"jan\",\"feb\",\"mar\"]");
    }
}
