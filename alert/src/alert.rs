extern crate reqwest;

use diesel::sqlite::SqliteConnection;
use crate::models::NewDollar;

use std::collections::HashMap;

pub fn new_data(conn: &SqliteConnection, new_data: &NewDollar) {
    let prc_change =
        match crate::storage::get_previous_dollar(conn) {
            Some(old_data) => (new_data.last - old_data.last)/old_data.last * 100.0,
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
    let client = reqwest::Client::new();
    let mut map = HashMap::new();
    map.insert("text", format!("Dollar changed {:+.2}%", prc_change));
    // TODO: Get Slack webhook URL from environment/argument/config
    client.post("https://hooks.slack.com/services/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")
        .json(&map)
        .send();
}

// fn send_alert_mail(prc_change: f64) {
//     let email = SendableEmail::new(
//         Envelope::new(
//             Some(EmailAddress::new("user@localhost".to_string()).unwrap()),
//             vec![EmailAddress::new("amin.arria@lambdaclass.com".to_string()).unwrap()],
//         ).unwrap(),
//         format!("id-{}", prc_change),
//         format!("Dolar changed: {}%", prc_change).into_bytes(),
//     );
//     let mut sender = SendmailTransport::new();
//     let mut sender = FileTransport::new("./tmp");
//     let result = sender.send(email);
//     assert!(result.is_ok());
// }
