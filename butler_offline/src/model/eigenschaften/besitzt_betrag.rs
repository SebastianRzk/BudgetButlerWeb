use crate::model::primitives::betrag::Betrag;

pub trait BesitztBetrag<'a> {
    fn betrag(&'a self) -> &'a Betrag;
}
