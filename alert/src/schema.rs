table! {
    dollar (id) {
        id -> Nullable<Integer>,
        buy -> Double,
        buy_amount -> Integer,
        sell -> Double,
        sell_amount -> Integer,
        last -> Double,
        var -> Double,
        varper -> Double,
        volume -> Integer,
        adjustment -> Double,
        min -> Double,
        max -> Double,
        oin -> Integer,
        created_at -> Timestamp,
    }
}
