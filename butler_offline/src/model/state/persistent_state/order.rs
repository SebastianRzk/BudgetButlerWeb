use crate::budgetbutler::database::change::change::{ChangeSelector, Creates};
use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::order::Order;
use crate::model::indiziert::Indiziert;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Orders {
    pub orders: Vec<Indiziert<Order>>,
}

impl Creates<Order, Orders> for Orders {
    fn create(item: Vec<Indiziert<Order>>) -> Orders {
        Orders { orders: item }
    }
}

impl Orders {
    pub fn select(&self) -> Selector<Indiziert<Order>> {
        Selector::new(self.orders.clone())
    }

    pub fn sort(&self) -> Orders {
        let mut neue_order = self.orders.clone();
        neue_order.sort();

        Orders { orders: neue_order }
    }

    pub fn get(&self, index: u32) -> Indiziert<Order> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn change(&self) -> ChangeSelector<Order, Orders> {
        ChangeSelector {
            content: self.orders.clone(),
            output: None,
        }
    }
}
