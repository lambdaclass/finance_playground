mod scrape;
mod storage;
mod alert;

use std::{fmt, thread, time};

pub struct DolarValue {
    buy: f64,
    buy_amount: u32,
    sell: f64,
    sell_amount: u32,
    last: f64,
    var: f64,
    varper: f64,
    volume: u32,
    adjustment: f64,
    min: f64,
    max: f64,
    oin: u32,
}

impl DolarValue {
    fn new() -> DolarValue {
        DolarValue {
            buy: 0.0,
            buy_amount: 0,
            sell: 0.0,
            sell_amount: 0,
            last: 0.0,
            var: 0.0,
            varper: 0.0,
            volume: 0,
            adjustment: 0.0,
            min: 0.0,
            max: 0.0,
            oin: 0,
        }
    }
}

impl fmt::Display for DolarValue {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "Buy: {}\nBuy Amount: {}\nSell: {}\nSell Amount: {}\nLast: {}\nVar: {}\nVarPer: {}\nVolume: {}\nAdjustment: {}\nMin: {}\nMax: {}\nOin: {}",
            self.buy, self.buy_amount, self.sell, self.sell_amount, self.last, self.var, self.varper, self.volume, self.adjustment, self.min, self.max, self.oin)
    }
}

fn main() {
    let dbconn = crate::storage::init();

    loop {
        let value = crate::scrape::scrape();
        crate::alert::new_data(&dbconn, &value);
        crate::storage::store(&dbconn, &value);

        println!("scraped dolar data");
        thread::sleep(time::Duration::from_secs(60));
    }
}
