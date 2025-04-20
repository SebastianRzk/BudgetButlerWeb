pub struct ETFName {
    pub name: String,
}

#[cfg(test)]
pub mod builder {
    use super::ETFName;

    pub fn etf_name(name: &str) -> ETFName {
        ETFName {
            name: name.to_string(),
        }
    }
}
