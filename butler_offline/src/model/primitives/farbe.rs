use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Farbe {
    pub as_string: String,
}

pub fn gray() -> Farbe {
    Farbe {
        as_string: "gray".to_string(),
    }
}

pub fn red() -> Farbe {
    Farbe {
        as_string: "red".to_string(),
    }
}

pub fn green() -> Farbe {
    Farbe {
        as_string: "lightgreen".to_string(),
    }
}

pub fn einnahmen_farbe() -> Farbe {
    Farbe {
        as_string: "rgb(210, 214, 222)".to_string(),
    }
}

pub fn ausgaben_farbe() -> Farbe {
    Farbe {
        as_string: "rgba(60,141,188,1)".to_string(),
    }
}

pub fn kontostand_farbe() -> Farbe {
    Farbe {
        as_string: "rgb(0, 166, 90)".to_string(),
    }
}

pub fn aufbuchungen_farbe() -> Farbe {
    Farbe {
        as_string: "rgb(60, 141, 188)".to_string(),
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::primitives::farbe::Farbe;

    pub fn farbe(farbe: &str) -> Farbe {
        Farbe {
            as_string: farbe.to_string(),
        }
    }

    pub fn any_farbe() -> Farbe {
        Farbe {
            as_string: "any_farbe".to_string(),
        }
    }
}
