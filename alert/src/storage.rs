extern crate diesel;
extern crate dotenv;

use diesel::prelude::*;
use diesel::sqlite::SqliteConnection;
use diesel::result::Error::NotFound;
use std::env;
use crate::models::{Dollar, NewDollar};
use crate::schema::dollar;

pub fn establish_connection() -> SqliteConnection {
    let database_url = env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");
    SqliteConnection::establish(&database_url)
        .expect(&format!("Error connecting to {}", database_url))
}

pub fn store(conn: &SqliteConnection, new_dollar: &NewDollar) {
    diesel::insert_into(dollar::table)
        .values(new_dollar)
        .execute(conn)
        .expect("Error saving new dollar");
}

pub fn get_previous_dollar(conn: &SqliteConnection) -> Option<Dollar> {
    let result = dollar::table.filter(dollar::buy_amount.gt(0))
        .order(dollar::buy_amount.desc())
        .first::<Dollar>(conn);

    match result {
        Ok(previous) => Some(previous),
        Err(NotFound) => None,
        Err(err) => panic!("Error getting previous dollar: \n{}", err)
    }
}
