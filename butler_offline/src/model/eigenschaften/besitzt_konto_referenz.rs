use crate::model::database::sparbuchung::KontoReferenz;

pub trait BesitztKontoReferenz<'a> {
    fn konto_referenz(&'a self) -> &'a KontoReferenz;
}
