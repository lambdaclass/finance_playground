#[macro_use]
extern crate diesel;
extern crate dotenv;
extern crate chrono;

pub mod schema;
pub mod models;

mod scrape;
mod storage;
mod alert;

use dotenv::dotenv;
use std::{thread, time};

fn main() {
    dotenv().ok();
    let dbconn = crate::storage::establish_connection();

    loop {
        let value = crate::scrape::scrape();
        crate::alert::new_data(&dbconn, &value);
        crate::storage::store(&dbconn, &value);

        thread::sleep(time::Duration::from_secs(60));
    }
}
