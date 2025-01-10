use diesel::result::Error;
use diesel::MysqlConnection;
use diesel_migrations::{embed_migrations, EmbeddedMigrations, MigrationHarness};

pub const MIGRATIONS: EmbeddedMigrations = embed_migrations!("migrations/");

pub fn run_migrations(connection: &mut MysqlConnection) -> Result<&str, Error> {
    connection
        .run_pending_migrations(MIGRATIONS)
        .expect("Failed to run migrations");
    Ok("")
}
