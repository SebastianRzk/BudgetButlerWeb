use crate::model::primitives::datum::Datum;

pub trait BesitztDatum<'a> {
    fn datum(&'a self) -> &'a Datum;
}
