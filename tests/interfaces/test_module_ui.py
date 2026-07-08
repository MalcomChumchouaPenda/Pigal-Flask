
import os
import pytest
from unittest.mock import MagicMock
from flask import Flask, Blueprint
from flask.views import View, MethodView
from pigal_flask import ModuleUi


def test_is_flask_blueprint():
    assert issubclass(ModuleUi, Blueprint)


@pytest.mark.parametrize('domain', [
    'home', 
    'auth', 
    'demo'
])
def test_is_configured_with_its_location(tmpdir, domain):
    test_dir = tmpdir / 'modules' / domain / 'views.py'
    location = test_dir.strpath
    ui = ModuleUi(location)

    assert ui.import_name == f'modules.{domain}.views'
    assert ui.template_folder == 'pages'
    assert ui.location == location
    assert ui.static_folder == location.replace('views.py', 'assets')
    assert ui.static_url_path == location.replace('views.py', 'assets')


@pytest.mark.parametrize('domain, url_prefix', [
    ('home', '/'), 
    ('auth', '/'), 
    ('demo', '/demo')
])
def test_generate_name_and_url_prefix(tmpdir, domain, url_prefix):
    test_dir = tmpdir / 'modules' / domain / 'views.py'
    location = test_dir.strpath
    ui = ModuleUi(location)  

    assert ui.name == domain
    assert ui.url_prefix == url_prefix


@pytest.fixture
def app(tmpdir):
    return Flask(__name__, 
                instance_path=tmpdir.strpath, 
                instance_relative_config=True)


def test_is_configured_by_location(tmpdir):
    location = tmpdir / 'modules' / 'demo' / 'views.py'
    location = location.strpath
    ui = ModuleUi(location)
    assert ui.location == location


@pytest.fixture
def ui(tmpdir):
    test_dir = tmpdir / 'modules' / 'demo' / 'views.py'
    location = test_dir.strpath
    return ModuleUi(location)


@pytest.fixture
def view_func(ui):
    @ui.route("/hello")
    def hello():
        return "Hello World"
    return hello


@pytest.mark.usefixtures('view_func')
def test_register_rules_for_simple_view_function(app, ui):
    app.register_blueprint(ui)
    rules = app.url_map.iter_rules()
    rules = {r.rule:r for r in rules}

    assert "/demo/hello" in rules
    assert 'GET' in rules["/demo/hello"].methods

    
@pytest.fixture
def view_func_with_methods(ui):
    @ui.route("/hello", methods=['GET', 'POST'])
    def hello():
        return "Hello World"
    return hello


@pytest.mark.usefixtures('view_func_with_methods')
def test_register_rules_for_class_based_view(app, ui):
    app.register_blueprint(ui)
    rules = app.url_map.iter_rules()
    rules = {r.rule:r for r in rules}

    assert "/demo/hello" in rules
    assert 'GET' in rules["/demo/hello"].methods
    assert 'POST' in rules["/demo/hello"].methods


@pytest.fixture
def view_cls(ui):
    @ui.route("/hello")
    class Demo(View):
        methods = ['GET', 'POST']
        def dispatch_request(self):
            return "Hello World"
    return Demo


@pytest.mark.usefixtures('view_cls')
def test_register_rules_for_class_based_view(app, ui):
    app.register_blueprint(ui)
    rules = app.url_map.iter_rules()
    rules = {r.rule:r for r in rules}

    assert "/demo/hello" in rules
    assert 'GET' in rules["/demo/hello"].methods
    assert 'POST' in rules["/demo/hello"].methods


@pytest.mark.usefixtures('view_cls')
def test_dispatch_request_to_class_based_view(app, ui):
    app.register_blueprint(ui)
    client = app.test_client()
    response = client.get("/demo/hello")

    assert response.status_code == 200
    assert response.data == b"Hello World"


@pytest.fixture
def method_view_cls(ui):
    @ui.route("/hello")
    class Demo(MethodView):
        def get(self):
            return "Hello World"               
        def post(self):
            pass
    return Demo


@pytest.mark.usefixtures('method_view_cls')
def test_register_route_for_method_view(app, ui):
    app.register_blueprint(ui)
    rules = app.url_map.iter_rules()
    rules = {r.rule:r for r in rules}
    
    assert "/demo/hello" in rules
    assert 'GET' in rules["/demo/hello"].methods
    assert 'POST' in rules["/demo/hello"].methods


@pytest.mark.usefixtures('method_view_cls')
def test_dispatch_request_to_method_view(app, ui):
    app.register_blueprint(ui)
    client = app.test_client()
    response = client.get("/demo/hello")

    assert response.status_code == 200
    assert response.data == b"Hello World"


@pytest.fixture
def file_based_view_cls(monkeypatch):
    import pigal_flask.__interfaces as pkg1
    import pigal_flask.views as pkg2
    
    class FakeView:
        routes = {}
        def __init__(self, location):
            self.location = location
            self.scan = MagicMock()
            self.as_view = MagicMock()

    monkeypatch.setattr(pkg1, 'FileBasedView', FakeView)
    monkeypatch.setattr(pkg2, 'FileBasedView', FakeView)
    return FakeView


def test_scan_routes_with_file_based_view(ui, file_based_view_cls):
    ui.scan()
    assert isinstance(ui.file_based_view, file_based_view_cls)
    assert ui.file_based_view.location == ui.location
    assert ui.file_based_view.scan.called
    

def test_scan_routes_and_register_urls(ui, file_based_view_cls):
    routes = {'/':'index.html', '/about':'about.html'}
    file_based_view_cls.routes = routes
    ui.add_url_rule = MagicMock()
    ui.scan()

    view_func = ui.file_based_view.as_view.return_value
    ui.file_based_view.as_view.assert_called_once_with("solve")
    ui.add_url_rule.assert_any_call('/', view_func=view_func)
    ui.add_url_rule.assert_any_call('/about', view_func=view_func)
    
