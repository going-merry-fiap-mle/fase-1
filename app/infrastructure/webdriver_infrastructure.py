from http import HTTPStatus

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from app.utils.environment_loader import EnvironmentLoader
from app.utils.logger import AppLogger


class WebDriverInfrastructure:

    def __init__(self, url: str = "https://books.toscrape.com/") -> None:
        self.logger = AppLogger("WebDriverInfrastructure")
        self.env_loader = EnvironmentLoader()

        self.url: str = url
        self.flask_env: str | None = None
        self.driver: webdriver.Firefox

        self.endless_loop_index: int = -1

        self._load_variables()
        self._driver_setup()

    def _driver_setup(self) -> None:
        self.logger.warning("Configurando o WebDriver...", HTTPStatus.CONTINUE)
        options = webdriver.FirefoxOptions()

        if self.flask_env != "dev":
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )

    def _load_variables(self) -> None:
        self.flask_env = self.env_loader.get("FLASK_ENV", "dev")
