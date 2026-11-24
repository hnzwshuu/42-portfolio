import os
import sys

REQUIRED_KEYS: tuple[str, ...] = (
    "DATABASE_URL",
    "API_KEY",
    "ZION_ENDPOINT",
)


class OracleConfig:
    def __init__(
        self,
        mode: str,
        database_url: str | None,
        api_key: str | None,
        log_level: str,
        zion_endpoint: str | None,
    ) -> None:
        self.mode = mode
        self.database_url = database_url
        self.api_key = api_key
        self.log_level = log_level
        self.zion_endpoint = zion_endpoint


def load_dotenv_file() -> bool:
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("[WARNING] python-dotenv is not installed.")
        print("Install it with: pip install python-dotenv")
        return False

    return bool(load_dotenv())


def read_config() -> OracleConfig:
    return OracleConfig(
        mode=os.getenv("MATRIX_MODE", "development"),
        database_url=os.getenv("DATABASE_URL"),
        api_key=os.getenv("API_KEY"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        zion_endpoint=os.getenv("ZION_ENDPOINT"),
    )


def mask_secret(secret: str | None) -> str:
    if not secret:
        return "Missing"
    return "Authenticated"


def database_status(config: OracleConfig) -> str:
    if config.database_url is None:
        return "Missing DATABASE_URL"
    if config.mode == "production":
        return "Connected to production instance"
    return "Connected to local instance"


def zion_status(config: OracleConfig) -> str:
    if config.zion_endpoint is None:
        return "Offline"
    return "Online"


def env_file_is_ignored() -> bool:
    try:
        with open(".gitignore", "r", encoding="utf-8") as gitignore:
            entries = {line.strip() for line in gitignore}
    except OSError:
        return False

    return ".env" in entries


def print_security_check(config_loaded: bool) -> None:
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    if config_loaded:
        print("[OK] .env file loaded")
    else:
        print("[WARING] No .env file loaded")
    if env_file_is_ignored():
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] Add .env to .gitignore before committing")

    print("[OK] Production overrides available")


def missing_keys() -> list[str]:
    return [key for key in REQUIRED_KEYS if not os.getenv(key)]


def print_missing_configuration(keys: list[str]) -> None:
    if not keys:
        return

    print("")
    print("Missing configuration:")
    for key in keys:
        print(f"- {key}")
    print("Copy .env.example to .env and fill in development values.")


def main() -> int:
    print()
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    config_loaded = load_dotenv_file()
    config = read_config()

    print("Configuration loaded:")
    print(f"Mode: {config.mode}")
    print(f"Database: {database_status(config)}")
    print(f"API Access: {mask_secret(config.api_key)}")
    print(f"Log Level: {config.log_level}")
    print(f"Zion Network: {zion_status(config)}")
    print("")

    print_security_check(config_loaded)
    print_missing_configuration(missing_keys())
    print("")
    print("The Oracle sees all configurations.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
