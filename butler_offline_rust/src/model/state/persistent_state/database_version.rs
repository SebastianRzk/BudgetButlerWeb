use rand::random;

#[derive(Clone, Debug, PartialEq)]
pub struct DatabaseVersion {
    pub name: String,
    pub version: u32,
    pub session_random: u32,
}

pub fn create_initial_database_version(name: String) -> DatabaseVersion {
    DatabaseVersion {
        name,
        version: 0,
        session_random: random(),
    }
}

impl DatabaseVersion {
    pub fn as_string(&self) -> String {
        format!("{}-{}-{}", self.name, self.version, self.session_random)
    }
    pub fn increment(&self) -> DatabaseVersion {
        DatabaseVersion {
            name: self.name.clone(),
            version: self.version + 1,
            session_random: self.session_random,
        }
    }
}
