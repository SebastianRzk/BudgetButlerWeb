use std::cmp::Ordering;

#[derive(Debug, Hash, Clone, PartialEq, Eq)]
pub struct Name {
    pub name: String,
}

impl Name {
    pub fn new(name: String) -> Name {
        Name { name }
    }

    pub fn get_name(&self) -> &String {
        &self.name
    }

    pub fn equals(&self, other: &Name) -> bool {
        self.name == other.name
    }

    pub fn to_string(&self) -> String {
        self.name.clone()
    }

    pub fn empty() -> Name {
        Name::new("".to_string())
    }
}

impl PartialOrd<Self> for Name {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Name {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.name.cmp(&other.name)
    }
}

pub fn name(name: &str) -> Name {
    Name::new(name.to_string())
}

#[cfg(test)]
pub mod builder {
    use crate::model::primitives::name::{name, Name};

    pub fn demo_name() -> Name {
        name("Test")
    }
}
