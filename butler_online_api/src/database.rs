use diesel::{r2d2, MysqlConnection};

pub type DbPool = r2d2::Pool<r2d2::ConnectionManager<MysqlConnection>>;
pub type DbError = Box<dyn std::error::Error + Send + Sync>;

pub fn initialize_db_pool() -> DbPool {
    let conn_spec = std::env::var("DATABASE_URL").expect("DATABASE_URL should be set");
    let manager = r2d2::ConnectionManager::<MysqlConnection>::new(conn_spec);
    r2d2::Pool::builder()
        .build(manager)
        .expect("DATABASE_URL should be valid url to a MySQL / MariaDB database")
}
