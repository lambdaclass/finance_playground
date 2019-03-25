extern crate fantoccini;
extern crate futures;
extern crate select;
extern crate serde_json;
extern crate tokio;
extern crate webdriver;

use fantoccini::{Client, Locator};
use futures::future::Future;
use futures::sync::oneshot;
use select::document::Document;
use select::predicate::Class;
use serde_json::json;
use webdriver::capabilities::Capabilities;
use std::{thread, time};

use crate::DolarValue;

pub fn scrape() -> DolarValue {
    let html = fetch_site();

    let document = Document::from(html.as_str());

    let mut value = DolarValue::new();

    for node in document.find(Class("PriceCell")) {
        match node.attr("class") {
            Some("PriceCell bsz") => value.buy_amount = parse_u32(node.text()),
            Some("PriceCell bid") => value.buy = parse_f64(node.text()),
            Some("PriceCell ask") => value.sell = parse_f64(node.text()),
            Some("PriceCell asz") => value.sell_amount = parse_u32(node.text()),
            Some("PriceCell lst") => value.last = parse_f64(node.text()),
            Some("PriceCell PriceCell-change-down variation") => value.var = parse_f64(node.text()),
            Some("PriceCell PriceCell-change-up variation") => value.var = parse_f64(node.text()),
            Some("PriceCell PriceCell-change-down change") => {
                value.varper = parse_f64(node.text().trim_end_matches("%").to_string())
            }
            Some("PriceCell PriceCell-change-up change") => {
                value.varper = parse_f64(node.text().trim_end_matches("%").to_string())
            }
            Some("PriceCell von") => value.volume = parse_u32(node.text()),
            Some("PriceCell settlementPrice") => value.adjustment = parse_f64(node.text()),
            Some("PriceCell PriceCell-none low") => value.min = parse_f64(node.text()),
            Some("PriceCell PriceCell-none hgh") => value.max = parse_f64(node.text()),
            Some("PriceCell oin") => value.oin = parse_u32(node.text()),
            Some("PriceCell futureImpliedRate") => {}
            Some(class) => {
                panic!("Non-matching class: {}", class);
            }
            None => {
                panic!("Node without class attribute");
            }
        }
    }

    value
}

fn fetch_site() -> String {
    let mut cap = Capabilities::new();
    let arg = json!({"args": ["-headless"]});
    cap.insert("moz:firefoxOptions".to_string(), arg);
    let c = Client::with_capabilities("http://localhost:4444", cap);
    let (sender, receiver) = oneshot::channel::<String>();

    tokio::run(
        c.map_err(|e| unimplemented!("failed to connect to WebDriver: {:?}", e))
            .and_then(|c| c.goto("https://rofex.primary.ventures/rofex/futuros"))
            .and_then(|mut c| c.current_url().map(move |url| (c, url)))
            .and_then(|(c, url)| {
                assert_eq!(url.as_ref(), "https://rofex.primary.ventures/rofex/futuros");
                c.wait_for_find(Locator::Css(".PricePanelRow-row"))
            })
            .and_then(|mut e| {
                // TODO: site has a small delay between creating the table and populating it
                //       this results in empty values ("-") causing an exception when parsing.
                //       We should handle this using a find or something instead of sleep
                thread::sleep(time::Duration::from_secs(1));
                e.html(true)
            })
            .and_then(|e| match sender.send(e) {
                Err(err) => panic!("Error sending fetched site: {}", err),
                Ok(()) => Ok(()),
            })
            .map_err(|e| {
                panic!("a WebDriver command failed: {:?}", e);
            }),
    );

    receiver.wait().unwrap()
}

fn parse_u32(text: String) -> u32 {
    text.replace(".", "")
        .trim()
        .parse()
        .unwrap_or_else(|err| panic!("Error parsing \"{}\": {}", text, err))
}

fn parse_f64(text: String) -> f64 {
    text.replace(".", "")
        .replace(",", ".")
        .trim()
        .parse()
        .unwrap_or_else(|err| panic!("Error parsing \"{}\": {}", text, err))
}
