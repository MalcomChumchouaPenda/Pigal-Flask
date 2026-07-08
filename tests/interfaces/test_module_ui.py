
import pytest
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

