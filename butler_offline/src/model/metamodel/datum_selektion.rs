use crate::model::primitives::datum::Datum;

pub struct DatumSelektion {
    pub datum: Datum,
    pub can_be_chosen: bool,
}

#[cfg(test)]
pub mod builder {
    use crate::model::metamodel::datum_selektion::DatumSelektion;
    use crate::model::primitives::datum::Datum;

    pub fn demo_datum_selektion_1() -> DatumSelektion {
        DatumSelektion {
            datum: Datum::new(1, 1, 2021),
            can_be_chosen: true,
        }
    }

    pub fn demo_datum_selektion_2() -> DatumSelektion {
        DatumSelektion {
            datum: Datum::new(01, 02, 2021),
            can_be_chosen: false,
        }
    }
}
