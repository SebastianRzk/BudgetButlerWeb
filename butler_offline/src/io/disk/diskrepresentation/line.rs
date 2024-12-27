#[derive(Debug, Clone, PartialEq)]
pub struct Line {
    pub line: String,
}

impl Line {
    pub fn new(line: &str) -> Line {
        Line {
            line: line.to_string(),
        }
    }

    pub fn empty_line() -> Line {
        Line {
            line: "".to_string(),
        }
    }
    pub fn from(string: String) -> Line {
        Line { line: string }
    }

    pub fn from_multiline_str(multiline_string: String) -> Vec<Line> {
        multiline_string
            .lines()
            .map(|line| Line::new(line))
            .collect()
    }
}

#[cfg(test)]
pub mod builder {
    use crate::io::disk::diskrepresentation::line::Line;

    pub fn line(line: &str) -> Line {
        Line {
            line: line.to_string(),
        }
    }

    pub fn as_string(lines: &Vec<Line>) -> String {
        lines
            .iter()
            .map(|line| line.line.clone())
            .collect::<Vec<String>>()
            .join("\n")
    }
}

pub fn as_string(lines: &Vec<Line>) -> String {
    lines
        .iter()
        .map(|line| line.line.clone())
        .collect::<Vec<String>>()
        .join("\n")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new() {
        let line = Line::new("asdf");
        assert_eq!(line.line, "asdf");
    }

    #[test]
    fn test_empty_line() {
        let line = Line::empty_line();
        assert_eq!(line.line, "");
    }

    #[test]
    fn test_from() {
        let line = Line::from("asdf".to_string());
        assert_eq!(line.line, "asdf");
    }

    #[test]
    fn test_from_multiline_str() {
        let multiline_string = "asdf\nqwer\nzxcv".to_string();
        let lines = Line::from_multiline_str(multiline_string);
        assert_eq!(lines.len(), 3);
        assert_eq!(lines[0].line, "asdf");
        assert_eq!(lines[1].line, "qwer");
        assert_eq!(lines[2].line, "zxcv");
    }
}
