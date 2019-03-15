extern crate tokio;
extern crate futures;
extern crate fantoccini;
extern crate webdriver;
extern crate serde_json;

use fantoccini::{Client, Locator};
use futures::future::Future;
use futures::sync::oneshot;
use webdriver::capabilities::Capabilities;
use serde_json::json;

fn main() {
    let html = fetch_site();
    println!("{}", html);
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
