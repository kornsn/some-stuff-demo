import pydantic


class Settings(pydantic.BaseSettings):
    db_server: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "some_stuff"
    testing: bool = False
    debug: bool = False

    api_key = "1234567asdfgh"
    api_key_name = "access_token"
    cookie_domain = "localtest.me"

    @property
    def db_url(self):
        if self.testing:
            db_name = self.test_db_name
        else:
            db_name = self.db_name
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_server}/{db_name}"

    @property
    def test_db_name(self):
        return "test_" + self.db_name


settings = Settings()
