use crate::io::disk::diskrepresentation::line::Line;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::name::Name;

const COMMA: char = ',';

pub fn read_next_element(zeile: Element) -> ParseErgebnis {
    let mut element = String::new();
    let mut quoted = false;
    let mut was_quoted = false;

    for char in zeile.element.chars() {
        if char == '"' {
            quoted = !quoted;
            was_quoted = true;
            continue;
        }
        if char == COMMA && !quoted {
            break;
        }
        element.push(char);
    }
    let rest;
    if was_quoted {
        rest = zeile
            .element
            .strip_prefix(&format!("\"{}\"", element))
            .unwrap();
    } else {
        rest = zeile.element.strip_prefix(&element).unwrap();
    }
    let rest = rest.strip_prefix(COMMA).unwrap_or_else(|| rest);
    ParseErgebnis {
        element: Element { element },
        rest: Element {
            element: rest.to_string(),
        },
    }
}

pub struct Element {
    pub element: String,
}

impl Into<Element> for &Line {
    fn into(self) -> Element {
        Element {
            element: self.line.clone(),
        }
    }
}

impl From<Name> for Element {
    fn from(name: Name) -> Self {
        Element {
            element: name.get_name().clone(),
        }
    }
}

impl From<KontoReferenz> for Element {
    fn from(konto_referenz: KontoReferenz) -> Self {
        Element {
            element: konto_referenz.konto_name.get_name().clone(),
        }
    }
}

impl Element {
    pub fn new(element: String) -> Element {
        Element { element }
    }

    pub fn create_escaped(element: String) -> Element {
        let element = element.clone().replace("\"", "");
        if element.contains(COMMA) {
            Element {
                element: format!("\"{}\"", element),
            }
        } else {
            Element { element }
        }
    }
}

pub struct ParseErgebnis {
    pub element: Element,
    pub rest: Element,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;

    #[test]
    fn test_read_next_element() {
        let ergebnis = read_next_element(element("2020-01-01,Rest"));
        assert_eq!(ergebnis.element.element, "2020-01-01");
        assert_eq!(ergebnis.rest.element, "Rest");
    }

    #[test]
    fn test_read_next_element_with_quoted_string() {
        let ergebnis = read_next_element(element("\"a string\",Rest"));
        assert_eq!(ergebnis.element.element, "a string");
        assert_eq!(ergebnis.rest.element, "Rest");
    }

    #[test]
    fn test_read_next_element_with_emojii() {
        let ergebnis = read_next_element(element("👍,Rest"));
        assert_eq!(ergebnis.element.element, "👍");
        assert_eq!(ergebnis.rest.element, "Rest");
    }

    #[test]
    fn test_create_escaped() {
        let element = Element::create_escaped("a string".to_string());
        assert_eq!(element.element, "a string");
    }

    #[test]
    fn test_create_escaped_with_comma() {
        let element = Element::create_escaped("a, string".to_string());
        assert_eq!(element.element, "\"a, string\"");
    }

    #[test]
    fn test_create_escaped_with_quotes() {
        let element = Element::create_escaped("\"a string\"".to_string());
        assert_eq!(element.element, "a string");
    }
}

#[cfg(test)]
pub mod builder {
    pub fn element(element: &str) -> super::Element {
        super::Element {
            element: element.to_string(),
        }
    }
}
