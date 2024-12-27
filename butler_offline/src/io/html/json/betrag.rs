use crate::model::primitives::betrag::Betrag;
use std::fmt::Display;

impl Display for Betrag {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}{}.{}", self.vorzeichen, self.euro, self.cent)
    }
}
