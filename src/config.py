import os


class Config:

    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))
    SERVER_CORS_ORIGINS = (
        "*"
        if os.getenv("SERVER_CORS_ORIGINS") in ["*", None]
        else os.getenv("SERVER_CORS_ORIGINS").split(";")
    )

    DB_ENGINE = os.getenv("DB_ENGINE", "sqlite-memory")

    if DB_ENGINE == "sqlite-memory":
        DB_URL = "sqlite:///:memory:"
    else:
        DB_URL = ""
