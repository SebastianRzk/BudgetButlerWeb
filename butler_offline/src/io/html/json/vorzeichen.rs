use crate::model::primitives::betrag::Vorzeichen;
use std::fmt::{Display, Formatter};

impl Display for Vorzeichen {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        if self == &Vorzeichen::Negativ {
            write!(f, "-")
        } else {
            write!(f, "")
        }
    }
}
