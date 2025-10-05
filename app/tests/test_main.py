from unittest.mock import MagicMock, patch

import pytest

from app.main import FlaskApp


@pytest.mark.parametrize(
    "env_values,expected",
    [
        (
            {"HOST": "127.0.0.1", "PORT": 8080, "DEBUG": True},
            {"host": "127.0.0.1", "port": 8080, "debug": True},
        ),
        (
            {"HOST": "192.168.1.10", "PORT": 5500, "DEBUG": True},
            {"host": "192.168.1.10", "port": 5500, "debug": True},
        ),
        ({}, {"host": "0.0.0.0", "port": 5000, "debug": False}),
    ],
)
def test_load_variables(env_values, expected) -> None:
    with patch("app.main.LogManager.setup"), patch("app.main.AppLogger"), patch(
        "app.main.EnvironmentLoader"
    ) as mock_env_loader_cls, patch("app.main.Flask"), patch("app.main.Swagger"), patch(
        "app.main.register_endpoints"
    ):
        loader = MagicMock()
        loader.get.side_effect = lambda key, default=None: env_values.get(key, default)
        mock_env_loader_cls.return_value = loader

        app = FlaskApp()

        assert app.host == expected["host"]
        assert app.port == expected["port"]
        assert app.debug == expected["debug"]


def test_run_calls_flask_run_with_loaded_config() -> None:
    with patch("app.main.LogManager.setup"), patch("app.main.AppLogger"), patch(
        "app.main.EnvironmentLoader"
    ) as mock_env_loader_cls, patch("app.main.Flask") as mock_flask_cls, patch(
        "app.main.Swagger"
    ), patch(
        "app.main.register_endpoints"
    ):
        loader = MagicMock()
        loader.get.side_effect = lambda key, default=None: {
            "HOST": "127.0.0.1",
            "PORT": 8080,
            "DEBUG": True,
        }.get(key, default)
        mock_env_loader_cls.return_value = loader

        app_mock = MagicMock()
        mock_flask_cls.return_value = app_mock

        app = FlaskApp()
        app.run()

        app_mock.run.assert_called_once_with(debug=True, host="127.0.0.1", port=8080)


def test_register_endpoints_called() -> None:
    with patch("app.main.LogManager.setup"), patch("app.main.AppLogger"), patch(
        "app.main.EnvironmentLoader"
    ) as mock_env_loader_cls, patch("app.main.Flask") as mock_flask_cls, patch(
        "app.main.Swagger"
    ), patch(
        "app.main.register_endpoints"
    ) as mock_register_endpoints:
        loader = MagicMock()
        loader.get.side_effect = lambda key, default=None: {
            "HOST": "0.0.0.0",
            "PORT": 5000,
            "DEBUG": False,
        }.get(key, default)
        mock_env_loader_cls.return_value = loader

        app_mock = MagicMock()
        mock_flask_cls.return_value = app_mock

        FlaskApp()

        mock_register_endpoints.assert_called_once_with(app_mock)


@pytest.mark.parametrize("port_value,raises", [("invalid_port", True), (5000, False)])
def test_run_raises_on_invalid_port(port_value, raises) -> None:
    with patch("app.main.LogManager.setup"), patch("app.main.AppLogger"), patch(
        "app.main.EnvironmentLoader"
    ) as mock_env_loader_cls, patch("app.main.Flask") as mock_flask_cls, patch(
        "app.main.Swagger"
    ), patch(
        "app.main.register_endpoints"
    ):
        loader = MagicMock()
        loader.get.side_effect = lambda key, default=None: {
            "HOST": "0.0.0.0",
            "PORT": port_value,
            "DEBUG": False,
        }.get(key, default)
        mock_env_loader_cls.return_value = loader

        app_mock = MagicMock()
        if raises:
            app_mock.run.side_effect = TypeError("port must be int")
        mock_flask_cls.return_value = app_mock

        app = FlaskApp()

        if raises:
            with pytest.raises(TypeError):
                app.run()
        else:
            app.run()
