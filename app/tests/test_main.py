from http import HTTPStatus
from unittest import mock
from unittest.mock import call, patch

import pytest
from flask import Flask

from app.main import FlaskApp, flask_app


def test_app_instance() -> None:
    assert isinstance(flask_app.app, Flask)


def test_blueprints_registered() -> None:
    blueprint_names = [bp.name for bp in flask_app.app.blueprints.values()]
    assert "books" in blueprint_names
    assert "categories" in blueprint_names
    assert "health" in blueprint_names


@pytest.mark.parametrize(
    "env_values,expected_host,expected_port,expected_debug",
    [
        ({"HOST": "127.0.0.1", "PORT": 8080, "DEBUG": True}, "127.0.0.1", 8080, True),
        ({"HOST": "0.0.0.0", "PORT": 5000, "DEBUG": False}, "0.0.0.0", 5000, False),
    ],
)
def test_run_uses_loaded_config_and_logs_info(
    env_values, expected_host, expected_port, expected_debug
):
    sequence = []

    def load_variable_side_effect(key, default):
        return env_values.get(key, default)

    def log_info_side_effect(message, status_code, **kwargs):
        sequence.append("log")

    def run_side_effect(*args, **kwargs):
        sequence.append("run")

    with patch("app.utils.logger.Logger.configure_with_os_variables"), patch(
        "app.utils.env_variables_loader.EnvVariablesLoader.load_variable",
        side_effect=load_variable_side_effect,
    ), patch("app.api.register_endpoints.register_endpoints"), patch(
        "flasgger.Swagger"
    ), patch(
        "app.utils.logger.Logger.log_info", side_effect=log_info_side_effect
    ) as mock_log_info, patch(
        "flask.Flask.run", side_effect=run_side_effect
    ) as mock_flask_run:

        app = FlaskApp()
        app.run()

        assert mock_log_info.call_args.args[0] == "Iniciando a aplicação..."
        assert mock_log_info.call_args.args[1] == HTTPStatus.CONTINUE

        assert mock_flask_run.call_args.kwargs["debug"] is expected_debug
        assert mock_flask_run.call_args.kwargs["host"] == expected_host
        assert mock_flask_run.call_args.kwargs["port"] == expected_port

        assert sequence == ["log", "run"]


@pytest.mark.parametrize(
    "env_values,expected_host,expected_port,expected_debug",
    [
        ({}, "0.0.0.0", 5000, False),
        (
            {"HOST": "127.0.0.1", "PORT": 8081, "DEBUG": True},
            "127.0.0.1",
            8081,
            True,
        ),
    ],
)
def test_load_variables(env_values, expected_host, expected_port, expected_debug):
    def load_variable_side_effect(key, default):
        return env_values.get(key, default)

    with patch("app.utils.logger.Logger.configure_with_os_variables"), patch(
        "app.api.register_endpoints.register_endpoints"
    ), patch("flasgger.Swagger"), patch(
        "app.utils.env_variables_loader.EnvVariablesLoader.load_variable",
        side_effect=load_variable_side_effect,
    ) as mock_load:

        app = FlaskApp()

        assert app.host == expected_host
        assert app.port == expected_port
        assert app.debug is expected_debug

        expected_calls = [
            call("HOST", "0.0.0.0"),
            call("PORT", 5000),
            call("DEBUG", False),
        ]
        mock_load.assert_has_calls(expected_calls)


@pytest.mark.parametrize(
    "bad_port",
    ["not-an-int", None, 3.14],
)
def test_run_with_invalid_port_raises_type_error(bad_port):
    def load_variable_side_effect(key, default):
        mapping = {"HOST": "0.0.0.0", "PORT": bad_port, "DEBUG": False}
        return mapping[key]

    with patch("app.utils.logger.Logger.configure_with_os_variables"), patch(
        "app.api.register_endpoints.register_endpoints"
    ), patch("flasgger.Swagger"), patch(
        "app.utils.env_variables_loader.EnvVariablesLoader.load_variable",
        side_effect=load_variable_side_effect,
    ), patch(
        "app.utils.logger.Logger.log_info"
    ), patch(
        "flask.Flask.run", side_effect=TypeError("port must be int")
    ):

        app = FlaskApp()
        with pytest.raises(TypeError, match="port must be int"):
            app.run()


@pytest.mark.parametrize(
    "exc_type,exc_msg",
    [
        (RuntimeError, "env error"),
        (KeyError, "missing variable"),
    ],
)
def test_init_propagates_env_loader_errors(exc_type, exc_msg):
    with patch("app.utils.logger.Logger.configure_with_os_variables"), patch(
        "app.utils.env_variables_loader.EnvVariablesLoader.load_variable",
        side_effect=exc_type(exc_msg),
    ):
        with pytest.raises(exc_type, match=exc_msg):
            FlaskApp()
