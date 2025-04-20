pub struct ETFIndex {
    pub name: String,
}

#[cfg(test)]
pub mod builder {
    use super::ETFIndex;

    pub fn etf_index(name: &str) -> ETFIndex {
        ETFIndex {
            name: name.to_string(),
        }
    }
}
