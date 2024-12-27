use crate::model::primitives::datum::Datum;

pub trait BesitztStartUndEndeDatum<'a> {
    fn start_datum(&'a self) -> &'a Datum;
    fn ende_datum(&'a self) -> &'a Datum;
}
