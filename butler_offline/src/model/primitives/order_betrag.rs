use crate::model::database::order::OrderTyp;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OrderBetrag {
    betrag: BetragOhneVorzeichen,
    order_typ: OrderTyp,
}

impl OrderBetrag {
    pub fn new(betrag: BetragOhneVorzeichen, order_typ: OrderTyp) -> OrderBetrag {
        OrderBetrag { betrag, order_typ }
    }

    pub fn get_betrag_fuer_geleistete_investition(&self) -> Betrag {
        match self.order_typ {
            OrderTyp::Kauf => self.betrag.positiv(),
            OrderTyp::Verkauf => self.betrag.negativ(),
            OrderTyp::Dividende => self.betrag.negativ(),
            OrderTyp::SonstigeKosten => self.betrag.positiv(),
            OrderTyp::Steuer => self.betrag.positiv(),
        }
    }

    pub fn get_realer_wert(&self) -> BetragOhneVorzeichen {
        self.betrag.clone()
    }

    pub fn get_typ(&self) -> OrderTyp {
        self.order_typ.clone()
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::database::order::OrderTyp::Kauf;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
    use crate::model::primitives::order_betrag::OrderBetrag;

    pub fn demo_order_betrag() -> OrderBetrag {
        OrderBetrag::new(u_zwei(), Kauf)
    }

    pub fn kauf(betrag: BetragOhneVorzeichen) -> OrderBetrag {
        OrderBetrag::new(betrag, Kauf)
    }

    pub fn verkauf(betrag: BetragOhneVorzeichen) -> OrderBetrag {
        OrderBetrag::new(betrag, crate::model::database::order::OrderTyp::Verkauf)
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::order::OrderTyp;
    use crate::model::primitives::betrag::Vorzeichen;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::primitives::order_betrag::OrderBetrag;

    #[test]
    fn test_get_betrag_fuer_geleistete_investition() {
        assert_eq!(
            to_buchung(OrderTyp::Kauf)
                .get_betrag_fuer_geleistete_investition()
                .vorzeichen,
            Vorzeichen::Positiv
        );
        assert_eq!(
            to_buchung(OrderTyp::Verkauf)
                .get_betrag_fuer_geleistete_investition()
                .vorzeichen,
            Vorzeichen::Negativ
        );
        assert_eq!(
            to_buchung(OrderTyp::SonstigeKosten)
                .get_betrag_fuer_geleistete_investition()
                .vorzeichen,
            Vorzeichen::Positiv
        );
        assert_eq!(
            to_buchung(OrderTyp::Dividende)
                .get_betrag_fuer_geleistete_investition()
                .vorzeichen,
            Vorzeichen::Negativ
        );
        assert_eq!(
            to_buchung(OrderTyp::Steuer)
                .get_betrag_fuer_geleistete_investition()
                .vorzeichen,
            Vorzeichen::Positiv
        );
    }

    fn to_buchung(typ: OrderTyp) -> OrderBetrag {
        OrderBetrag::new(u_zwei(), typ)
    }
}
