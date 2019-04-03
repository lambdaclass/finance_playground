extern crate diesel;
extern crate dotenv;

use diesel::prelude::*;
use diesel::sqlite::SqliteConnection;
use diesel::result::Error::NotFound;
use chrono::{Utc, NaiveDateTime, NaiveTime};
use std::env;
use crate::models::{Dollar, NewDollar};
use crate::schema::dollar;

pub fn establish_connection() -> SqliteConnection {
    // We can unwrap safely because env variables are checking in main.rs::init_env()
    let database_url = env::var("DATABASE_URL").unwrap();
    SqliteConnection::establish(&database_url)
        .expect(&format!("Error connecting to {}", database_url))
}

pub fn store(conn: &SqliteConnection, new_dollar: &NewDollar) {
    diesel::insert_into(dollar::table)
        .values(new_dollar)
        .execute(conn)
        .expect("Error saving new dollar");
}

pub fn get_dollar_on_close(conn: &SqliteConnection) -> Option<Dollar> {
    let yesterday = Utc::today().naive_utc().pred();
    let timestamp = NaiveDateTime::new(yesterday, NaiveTime::from_hms(23, 59, 59));

    let result = dollar::table.filter(dollar::created_at.lt(timestamp))
        .order(dollar::created_at.desc())
        .first::<Dollar>(conn);

    match result {
        Ok(previous) => Some(previous),
        Err(NotFound) => None,
        Err(err) => panic!("Error getting previous dollar: \n{}", err)
    }
}
