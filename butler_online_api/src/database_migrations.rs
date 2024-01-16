use diesel_migrations::{embed_migrations, EmbeddedMigrations, MigrationHarness};
use diesel::MysqlConnection;
use diesel::result::Error;

pub const MIGRATIONS: EmbeddedMigrations = embed_migrations!("migrations/");


pub fn run_migrations(connection: &mut MysqlConnection) -> Result<&str, Error> {

    connection.run_pending_migrations(MIGRATIONS).unwrap();

    Ok("")
}