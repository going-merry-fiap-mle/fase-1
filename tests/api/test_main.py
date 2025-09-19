from api.main import app
from flask import Flask

def test_app_instance():
    assert isinstance(app, Flask)

def test_blueprints_registered():
    blueprint_names = [bp.name for bp in app.blueprints.values()]
    assert 'books' in blueprint_names
    assert 'categories' in blueprint_names
    assert 'health' in blueprint_names

