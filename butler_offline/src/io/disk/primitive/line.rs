use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::primitive::segment_reader::Element;

pub fn create_line(elements: Vec<Element>) -> Line {
    let elements_unpacked: Vec<String> = elements.iter().map(|x| x.element.clone()).collect();
    Line {
        line: elements_unpacked.join(","),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;

    #[test]
    fn test_create_line() {
        let elements = vec![element("2020-01-01"), element("Rest")];
        let line = create_line(elements);
        assert_eq!(line.line, "2020-01-01,Rest");
    }
}
