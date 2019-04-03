.PHONY: migration run install_diesel_cli

migration:
	diesel migration run

run:
	cargo run

install_diesel_cli:
	cargo install diesel_cli --no-default-features --features sqlite chrono
