use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Hash, Eq, Serialize, Deserialize)]
pub struct Person {
    pub person: String,
}

impl Person {
    pub fn new(person: String) -> Person {
        Person { person }
    }

    pub fn empty() -> Person {
        Person {
            person: "".to_string(),
        }
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::primitives::person::Person;

    pub fn person(person: &str) -> Person {
        Person::new(person.to_string())
    }

    pub fn demo_person() -> Person {
        person("Test_User")
    }

    pub fn demo_self() -> Person {
        person("Self")
    }

    pub fn demo_partner() -> Person {
        person("Partner")
    }

    pub fn demo_partner_str() -> String {
        "Partner".to_string()
    }
}
