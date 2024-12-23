use crate::model::database::order::OrderTyp;
use crate::model::primitives::betrag::Betrag;
use crate::model::state::persistent_application_state::Database;

pub struct OrderTypen {
    pub gesamt_dynamisch: Betrag,
    pub gesamt_statisch: Betrag,
}

pub fn berechne_order_typen(database: &Database) -> OrderTypen {
    let selector = database
        .order
        .select()
        .filter(|y| y.value.wert.get_typ() == OrderTyp::Kauf);

    OrderTypen {
        gesamt_dynamisch: selector
            .clone()
            .filter(|x| x.dynamisch)
            .map(|x| x.value.wert.get_realer_wert().positiv())
            .bilde_summe(),
        gesamt_statisch: selector
            .clone()
            .filter(|x| !x.dynamisch)
            .map(|x| x.value.wert.get_realer_wert().positiv())
            .bilde_summe(),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_calculations::order_typen::berechne_order_typen;
    use crate::model::database::depotwert::builder::demo_depotwert_referenz;
    use crate::model::database::order::Order;
    use crate::model::database::sparbuchung::builder::demo_konto_referenz;
    use crate::model::indiziert::builder::{dynamisch_indiziert, indiziert};
    use crate::model::primitives::betrag::builder::u_betrag;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::order_betrag::builder::kauf;
    use crate::model::state::persistent_application_state::builder::generate_empty_database;
    use crate::model::state::persistent_state::order::Orders;

    #[test]
    fn test_berechne_order_typen_mit_leer_db() {
        let result = berechne_order_typen(&generate_empty_database());

        assert_eq!(result.gesamt_dynamisch, Betrag::zero());
        assert_eq!(result.gesamt_statisch, Betrag::zero());
    }

    #[test]
    fn test_berechne_order_typen() {
        let result = berechne_order_typen(&generate_empty_database().change_order(Orders {
            orders: vec![
                indiziert(Order {
                    wert: kauf(u_betrag(150, 0)),
                    name: demo_name(),
                    konto: demo_konto_referenz(),
                    depotwert: demo_depotwert_referenz(),
                    datum: any_datum(),
                }),
                dynamisch_indiziert(Order {
                    wert: kauf(u_betrag(50, 0)),
                    name: demo_name(),
                    konto: demo_konto_referenz(),
                    depotwert: demo_depotwert_referenz(),
                    datum: any_datum(),
                }),
            ],
        }));

        assert_eq!(
            result.gesamt_statisch,
            Betrag::from_cent(Vorzeichen::Positiv, 15000)
        );
        assert_eq!(
            result.gesamt_dynamisch,
            Betrag::from_cent(Vorzeichen::Positiv, 5000)
        );
    }
}
