use crate::model::primitives::datum::Datum;

pub mod gemeinsam_abrechnen;
pub mod persoenliche_buchungen_abrechnen;

pub struct AbrechnungZeitlicheRahmendaten {
    pub start_datum: Datum,
    pub ende_datum: Datum,
    pub heute: Datum,
}
