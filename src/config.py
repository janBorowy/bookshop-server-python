from os import environ

def get_env(key: str):
    return environ.get(key)

class Config:
    def __init__(self, db_name="", db_username="", db_password="", db_host="", port="", host="") -> None:
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password
        self.db_host = db_host
        self.port = int(port)
        self.host = host

config = Config(
    db_name=get_env("DB_NAME"),
    db_username=get_env("DB_USERNAME"),
    db_password=get_env("DB_PASSWORD"),
    db_host=get_env("DB_HOST"),
    port=get_env("PORT"),
    host=get_env("HOST")
)
