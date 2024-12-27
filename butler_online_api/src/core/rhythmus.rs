#[derive(PartialEq, Clone)]
pub enum Rhythmus {
    Monatlich,
    ViertelJaehrlich,
    HalbJaehrlich,
    Jaehrlich,
}

const RHYTHMUS_MONATLICH: &str = "monatlich";
const RHYTHMUS_VIERTEL_JAEHRLICH: &str = "viertel_jaehrlich";
const RHYTHMUS_HALB_JAEHRLICH: &str = "halb_jaehrlich";
const RHYTHMUS_JAEHRLICH: &str = "jaehrlich";

impl Rhythmus {
    pub fn to_string(&self) -> String {
        match self {
            Rhythmus::Monatlich => RHYTHMUS_MONATLICH.to_string(),
            Rhythmus::ViertelJaehrlich => RHYTHMUS_VIERTEL_JAEHRLICH.to_string(),
            Rhythmus::HalbJaehrlich => RHYTHMUS_HALB_JAEHRLICH.to_string(),
            Rhythmus::Jaehrlich => RHYTHMUS_JAEHRLICH.to_string(),
        }
    }
}

pub fn rhythmus_from_string(s: String) -> Result<Rhythmus, ()> {
    match s.as_str() {
        RHYTHMUS_MONATLICH => Ok(Rhythmus::Monatlich),
        RHYTHMUS_VIERTEL_JAEHRLICH => Ok(Rhythmus::ViertelJaehrlich),
        RHYTHMUS_HALB_JAEHRLICH => Ok(Rhythmus::HalbJaehrlich),
        RHYTHMUS_JAEHRLICH => Ok(Rhythmus::Jaehrlich),
        _ => Err(()),
    }
}
