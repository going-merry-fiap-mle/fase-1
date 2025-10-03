from http import HTTPStatus

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from app.utils.env_variables_loader import EnvVariablesLoader
from app.utils.logger import Logger


class WebDriverService:

    def __init__(self, url: str = "https://books.toscrape.com/") -> None:
        self.logger = Logger("WebDriverService")
        self.env_loader = EnvVariablesLoader()

        self.url: str = url
        self.flask_env: str | None = None
        self.driver: webdriver.Firefox

        self.endless_loop_index: int = -1

        self._load_variables()
        self._driver_setup()

    def _driver_setup(self) -> None:
        self.logger.log_info("Configurando o WebDriver...", HTTPStatus.CONTINUE)
        options = webdriver.FirefoxOptions()

        if self.flask_env != "dev":
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )

    def _load_variables(self) -> None:
        self.flask_env = self.env_loader.load_variable("FLASK_ENV", "dev")
