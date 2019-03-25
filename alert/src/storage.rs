extern crate rusqlite;

use rusqlite::{Connection, ToSql, NO_PARAMS};
use crate::DolarValue;

pub fn init() -> Connection {
    let conn = Connection::open("./alert.db")
        .unwrap_or_else(|err| panic!("Error connecting to SQLite DB: {}", err));

    conn.execute(
        "CREATE TABLE IF NOT EXISTS dolar (
            id              INTEGER PRIMARY KEY,
            buy             DOUBLE NOT NULL,
            buy_amount      INTEGER NOT NULL,
            sell            DOUBLE NOT NULL,
            sell_amount     INTEGER NOT NULL,
            last            DOUBLE NOT NULL,
            var             DOUBLE NOT NULL,
            varper          DOUBLE NOT NULL,
            volume          INTEGER NOT NULL,
            adjustment      DOUBLE NOT NULL,
            min             DOUBLE NOT NULL,
            max             DOUBLE NOT NULL,
            oin             INTEGER NOT NULL,
            created_at      DATETIME NOT NULL
        )",
        NO_PARAMS,
    ).unwrap_or_else(|err| panic!("Error creating table \"dolar\": {}", err));

    conn
}

pub fn store(conn: &Connection, data: DolarValue) {
    conn.execute(
        "INSERT INTO dolar (buy, buy_amount, sell, sell_amount, last, var, varper, volume, adjustment, min, max, oin, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))",
        &[&data.buy as &ToSql,
          &data.buy_amount,
          &data.sell,
          &data.sell_amount,
          &data.last,
          &data.var,
          &data.varper,
          &data.volume,
          &data.adjustment,
          &data.min,
          &data.max,
          &data.oin]
    ).unwrap();
}
