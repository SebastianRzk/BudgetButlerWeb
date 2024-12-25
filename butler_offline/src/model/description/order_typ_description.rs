use crate::model::database::order::OrderTyp;
use crate::model::primitives::type_description::TypeDescription;

pub fn get_all_order_typ_descriptions() -> Vec<TypeDescription<OrderTyp>> {
    vec![
        TypeDescription {
            value: OrderTyp::Kauf,
            description: "Kauf".to_string(),
        },
        TypeDescription {
            value: OrderTyp::Verkauf,
            description: "Verkauf".to_string(),
        },
        TypeDescription {
            value: OrderTyp::Steuer,
            description: "Steuer (z.B. Vorabpauschale)".to_string(),
        },
        TypeDescription {
            value: OrderTyp::Dividende,
            description: "Dividende".to_string(),
        },
        TypeDescription {
            value: OrderTyp::SonstigeKosten,
            description: "Sonstige Kosten".to_string(),
        },
    ]
}
