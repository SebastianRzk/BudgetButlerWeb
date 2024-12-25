#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Rhythmus {
    Monatlich,
    Vierteljaehrlich,
    Halbjaehrlich,
    Jaehrlich,
}

impl Rhythmus {
    pub fn to_german_string(&self) -> String {
        match self {
            Rhythmus::Monatlich => "monatlich".to_string(),
            Rhythmus::Vierteljaehrlich => "vierteljährlich".to_string(),
            Rhythmus::Halbjaehrlich => "halbjährlich".to_string(),
            Rhythmus::Jaehrlich => "jährlich".to_string(),
        }
    }

    pub fn from_german_string(string: &String) -> Rhythmus {
        match string.as_str() {
            "monatlich" => Rhythmus::Monatlich,
            "vierteljährlich" => Rhythmus::Vierteljaehrlich,
            "halbjährlich" => Rhythmus::Halbjaehrlich,
            "jährlich" => Rhythmus::Jaehrlich,
            _ => panic!("Invalid rhythmus string: {}", string),
        }
    }
}
