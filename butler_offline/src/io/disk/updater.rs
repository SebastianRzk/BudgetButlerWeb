use crate::io::disk::reader::read_database;
use crate::io::disk::writer::write_database;
use crate::model::state::config::DatabaseConfiguration;
use crate::model::state::persistent_application_state::Database;

pub fn update_database(config: &DatabaseConfiguration, current_database: Database) -> Database {
    write_database(&current_database, config);
    read_database(config, current_database.db_version.increment())
}
