use chrono::NaiveDateTime;
use chrono::offset::Utc;
use crate::schema::dollar;

#[derive(Queryable)]
pub struct Dollar {
    pub id: Option<i32>,
    pub buy: f64,
    pub buy_amount: i32,
    pub sell: f64,
    pub sell_amount: i32,
    pub last: f64,
    pub var: f64,
    pub varper: f64,
    pub volume: i32,
    pub adjustment: f64,
    pub min: f64,
    pub max: f64,
    pub oin: i32,
    pub created_at: NaiveDateTime
}

#[derive(Insertable)]
#[table_name="dollar"]
pub struct NewDollar {
    pub buy: f64,
    pub buy_amount: i32,
    pub sell: f64,
    pub sell_amount: i32,
    pub last: f64,
    pub var: f64,
    pub varper: f64,
    pub volume: i32,
    pub adjustment: f64,
    pub min: f64,
    pub max: f64,
    pub oin: i32,
    pub created_at: NaiveDateTime
}

impl NewDollar {
    pub fn new() -> NewDollar {
        let now = Utc::now();
        let created_at = NaiveDateTime::from_timestamp(now.timestamp(), 0);

        NewDollar {
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
            created_at: created_at
        }
    }
}
