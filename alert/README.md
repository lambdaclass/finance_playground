# Financial Watchdog

## Requirements
- [WebDriver](https://www.w3.org/TR/webdriver1/) process running on port 4444 (e.g., [geckodriver](https://github.com/mozilla/geckodriver/releases), [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/))
- SQLite 3.19.3
- Rust 1.33
- [Diesel CLI 1.4](https://crates.io/crates/diesel_cli)

When installing `diesel_cli` if you run into any errors try the needed features using this command:

```
$> make install_diesel_cli
```

## Running

First create the database

```
$> make migration
```

Run it

```
$> make run
```
