use crate::model::primitives::kategorie::Kategorie;

pub trait BesitztKategorie<'a> {
    fn kategorie(&'a self) -> &'a Kategorie;
}
