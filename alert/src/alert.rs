extern crate reqwest;

use diesel::sqlite::SqliteConnection;
use std::collections::HashMap;
use std::env;
use crate::models::{Dollar, Alert};
use crate::storage;

pub fn check_dollar(conn: &SqliteConnection, dollar: &Dollar) {
    let dollar_close = storage::get_dollar_on_close(conn);
    let closing_prc_change =
        match &dollar_close {
            Some(dollar_close) => {
                (dollar.last - dollar_close.last)/dollar_close.last * 100.0
            },
            None => 0.0
        };

    match storage::get_dollar_alert(conn) {
        Some(dollar_alert) => {
            let alert_prc_change = (dollar.last - dollar_alert.current_value)/dollar_alert.current_value * 100.0;
            // TODO: This value should be set by arguments to binary or by config files
            if alert_prc_change.abs() > 2.0 {
                if closing_prc_change.abs() > 3.0 {
                    send_updated_alert(alert_prc_change);
                } else {
                    storage::deactivate_alert(conn, &dollar_alert);
                    send_resolved_alert();
                }
            }
        }
        None => {
            // TODO: This value should be set by arguments to binary or by config files
            if closing_prc_change.abs() > 3.0 {
                // If we couldn't unwrap closing_prc_change == 0.0
                let dollar_close = dollar_close.unwrap();
                let alert = Alert::new(String::from("dollar"), dollar_close.last, dollar.last);
                storage::store_alert(conn, &alert);
                send_new_alert(closing_prc_change);
            }
        }
    };
}

fn send_new_alert(prc_change: f64) {
    let msg = format!("Dollar price changed {:+.2}%", prc_change);
    send_alert_slack(msg);
    // TODO: send_alert_mail(prc_change);
}

fn send_resolved_alert() {
    let msg = format!("Dollar price change is below threshold");
    send_alert_slack(msg);
    // TODO: send_alert_mail(prc_change);
}

fn send_updated_alert(prc_change: f64) {
    let msg = format!("[UPDATE] Dollar price changed {:+.2}%", prc_change);
    send_alert_slack(msg);
    // TODO: send_alert_mail(prc_change);
}

fn send_alert_slack(msg: String) {
    // We can unwrap safely because env variables are checked in main.rs::init_env()
    let slack_webhook_url = env::var("SLACK_WEBHOOK_URL").unwrap();
    let client = reqwest::Client::new();
    let mut map = HashMap::new();
    map.insert("text", msg);
    client.post(&slack_webhook_url)
        .json(&map)
        .send()
        .expect("Failed sending slack alert");
}
