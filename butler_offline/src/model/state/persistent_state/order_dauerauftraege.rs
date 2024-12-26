use crate::budgetbutler::database::change::change::{ChangeSelector, Creates};
use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
use crate::model::indiziert::Indiziert;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct OrderDauerauftraege {
    pub order_dauerauftraege: Vec<Indiziert<OrderDauerauftrag>>,
}

impl Creates<OrderDauerauftrag, OrderDauerauftraege> for OrderDauerauftraege {
    fn create(item: Vec<Indiziert<OrderDauerauftrag>>) -> OrderDauerauftraege {
        OrderDauerauftraege {
            order_dauerauftraege: item,
        }
    }
}

impl OrderDauerauftraege {
    pub fn select(&self) -> Selector<Indiziert<OrderDauerauftrag>> {
        Selector::new(self.order_dauerauftraege.clone())
    }

    pub fn sort(&self) -> OrderDauerauftraege {
        let mut neue_order_dauerauftraege = self.order_dauerauftraege.clone();
        neue_order_dauerauftraege.sort();

        OrderDauerauftraege {
            order_dauerauftraege: neue_order_dauerauftraege,
        }
    }

    pub fn get(&self, index: u32) -> Indiziert<OrderDauerauftrag> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn change(&self) -> ChangeSelector<OrderDauerauftrag, OrderDauerauftraege> {
        ChangeSelector {
            content: self.order_dauerauftraege.clone(),
            output: None,
        }
    }
}
