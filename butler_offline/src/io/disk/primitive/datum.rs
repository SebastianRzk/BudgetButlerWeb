use crate::io::disk::primitive::segment_reader::Element;
use crate::model::primitives::datum::Datum;

pub fn read_datum(datum: Element) -> Datum {
    Datum::from_iso_string(&datum.element)
}

pub fn write_datum(datum: &Datum) -> Element {
    Element {
        element: datum.to_iso_string(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;

    #[test]
    fn test_read_datum() {
        let ergebnis = read_datum(element("2020-01-01"));
        assert_eq!(ergebnis, Datum::new(1, 1, 2020));
    }
}
