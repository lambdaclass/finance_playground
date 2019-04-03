extern crate reqwest;

use diesel::sqlite::SqliteConnection;
use std::collections::HashMap;
use std::env;
use crate::models::Dollar;
use crate::storage;

pub fn new_data(conn: &SqliteConnection, new_data: &Dollar) {
    let prc_change =
        match storage::get_dollar_on_close(conn) {
            Some(old_data) => {
                (new_data.last - old_data.last)/old_data.last * 100.0
            },
            None => 0.0
        };

    // TODO: This value should be set by arguments to binary or by config files
    if prc_change.abs() > 1.0 {
        send_alert(prc_change);
    }
}

fn send_alert(prc_change: f64) {
    send_alert_slack(prc_change);
    // TODO: send_alert_mail(prc_change);
}

fn send_alert_slack(prc_change: f64) {
    // We can unwrap safely because env variables are checking in main.rs::init_env()
    let slack_webhook_url = env::var("DATABASE_URL").unwrap();
    let client = reqwest::Client::new();
    let mut map = HashMap::new();
    map.insert("text", format!("Dollar changed {:+.2}%", prc_change));
    client.post(&slack_webhook_url)
        .json(&map)
        .send();
}
