use diesel::{MysqlConnection, r2d2};

use crate::DbPool;

pub fn initialize_db_pool() -> DbPool {
    let conn_spec = std::env::var("DATABASE_URL").expect("DATABASE_URL should be set");
    let manager = r2d2::ConnectionManager::<MysqlConnection>::new(conn_spec);
    r2d2::Pool::builder()
        .build(manager)
        .expect("DATABASE_URL should be valid url to a MySQL / MariaDB database")
}
