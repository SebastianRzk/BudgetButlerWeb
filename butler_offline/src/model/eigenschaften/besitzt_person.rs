use crate::model::primitives::person::Person;

pub trait BesitztPerson<'a> {
    fn person(&'a self) -> &'a Person;
}
