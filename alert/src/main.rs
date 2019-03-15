extern crate tokio;
extern crate futures;
extern crate fantoccini;
extern crate webdriver;
extern crate serde_json;
extern crate select;

use fantoccini::{Client, Locator};
use futures::future::Future;
use futures::sync::oneshot;
use webdriver::capabilities::Capabilities;
use serde_json::json;
use select::document::Document;
use select::predicate::{Predicate, Attr, Class, Name};

struct DolarValue {
    buy: f64,
    buyamount: u32,
    sell: f64,
    sellamount: u32,
    last: f64,
    var: f64,
    varper: f64,
    volume: u32,
    adjustment: f64,
    min: f64,
    max: f64,
    oin: u32,
}

fn main() {
    let html = fetch_site();

    let document = Document::from(html.as_str());

    // let mut values = DolarValue {};

    for node in document.find(Class("PriceCell")) {
        match node.attr("class") {
            Some("PriceCell bsz") => {
                println!("BuyAmount: {}", node.text())
            },
            Some("PriceCell bid") => {
                println!("Buy: {}", node.text())
            },
            Some("PriceCell ask") => {
                println!("Sell: {}", node.text())
            },
            Some("PriceCell asz") => {
                println!("SellAmount: {}", node.text())
            },
            Some("PriceCell lst") => {
                println!("Last: {}", node.text())
            },
            Some("PriceCell PriceCell-change-down variation") => {
                println!("Var: {}", node.text())
            },
            Some("PriceCell PriceCell-change-up variation") => {
                println!("Var: {}", node.text())
            },
            Some("PriceCell PriceCell-change-down change") => {
                println!("VarPer: {}", node.text())
            },
            Some("PriceCell PriceCell-change-up change") => {
                println!("VarPer: {}", node.text())
            },
            Some("PriceCell von") => {
                println!("Volume: {}", node.text())
            },
            Some("PriceCell settlementPrice") => {
                println!("Adjustment: {}", node.text())
            },
            Some("PriceCell PriceCell-none low") => {
                println!("Min: {}", node.text())
            },
            Some("PriceCell PriceCell-none hgh") => {
                println!("Max: {}", node.text())
            },
            Some("PriceCell oin") => {
                println!("Oin: {}", node.text())
            },
            Some("PriceCell futureImpliedRate") => { },
            Some(class) => {
                panic!("Non-matching class: {}", class);
            }
            None => {
                panic!("Node without class attribute");
            }
        }
    }
}

fn fetch_site() -> String {
    let mut cap = Capabilities::new();
    let arg = json!({"args": ["-headless"]});
    cap.insert("moz:firefoxOptions".to_string(), arg);
    let c = Client::with_capabilities("http://localhost:4444", cap);
    let (sender, receiver) = oneshot::channel::<String>();

    tokio::run(
        c
            .map_err(|e| {
                unimplemented!("failed to connect to WebDriver: {:?}", e)
            })
            .and_then(|c| {
                c.goto("https://rofex.primary.ventures/rofex/futuros")
            })
            .and_then(|mut c| c.current_url().map(move |url| (c, url)))
            .and_then(|(c, url)| {
                assert_eq!(url.as_ref(), "https://rofex.primary.ventures/rofex/futuros");
                c.wait_for_find(Locator::Css(".PricePanelRow-row"))
            })
            .and_then(|mut e| {
                e.html(true)
            })
            .and_then(|e| {
                sender.send(e);
                Ok(())
            })
            .map_err(|e| {
                panic!("a WebDriver command failed: {:?}", e);
            })
    );

    receiver.wait().unwrap()
}
