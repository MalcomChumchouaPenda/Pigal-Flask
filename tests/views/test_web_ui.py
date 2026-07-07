
import pytest
from flask import Flask, Blueprint
from flask.views import View, MethodView
from pigal_flask.views import WebUi


def test_is_flask_blueprint():
    assert issubclass(WebUi, Blueprint)


@pytest.fixture
def views_file(tmpdir):
    test_dir = tmpdir / 'modules' / 'demo' / 'views.py'
    return test_dir.strpath



def test_is_configured_with_views_file(views_file):
    ui = WebUi(views_file)
    assert ui.import_name == 'modules.demo.views'
    assert ui.template_folder == 'pages'
    assert ui.static_folder == views_file.replace('views.py', 'assets')
    assert ui.static_url_path == views_file.replace('views.py', 'assets')


@pytest.mark.parametrize('domain, url_prefix', [
    ('home', '/'), 
    ('auth', '/'), 
    ('demo', '/demo')
])
def test_generate_name_and_url_prefix(tmpdir, domain, url_prefix):
    test_dir = tmpdir / 'modules' / domain / 'views.py'
    views_file = test_dir.strpath
    ui = WebUi(views_file)    
    assert ui.name == domain
    assert ui.url_prefix == url_prefix


@pytest.fixture
def app(tmpdir):
    return Flask(__name__, 
                instance_path=tmpdir.strpath, 
                instance_relative_config=True)


@pytest.fixture
def view_cls(app, views_file):
    ui = WebUi(views_file)

    @ui.route("/hello")
    class Demo(View):
        methods = ['GET', 'POST']
        def dispatch_request(self):
            return "Hello World"
        
    app.register_blueprint(ui)
    return Demo


@pytest.mark.usefixtures('view_cls')
def test_register_route_for_class_based_view(app):
    rules = {rule.rule:rule for rule in app.url_map.iter_rules()}
    assert "/demo/hello" in rules
    assert 'GET' in rules["/demo/hello"].methods
    assert 'POST' in rules["/demo/hello"].methods


@pytest.mark.usefixtures('view_cls')
def test_dispatch_request_to_class_based_view(app):
    client = app.test_client()
    response = client.get("/demo/hello")
    assert response.status_code == 200
    assert response.data == b"Hello World"


@pytest.fixture
def method_view_cls(app, views_file):
    ui = WebUi(views_file)

    @ui.route("/hello")
    class Demo(MethodView):
        def get(self):
            return "Hello World"
        
        def post(self):
            pass
        
    app.register_blueprint(ui)
    return Demo


@pytest.mark.usefixtures('method_view_cls')
def test_register_route_for_method_view(app):
    rules = {rule.rule:rule for rule in app.url_map.iter_rules()}
    assert "/demo/hello" in rules
    assert 'GET' in rules["/demo/hello"].methods
    assert 'POST' in rules["/demo/hello"].methods


@pytest.mark.usefixtures('method_view_cls')
def test_dispatch_request_to_method_view(app):
    client = app.test_client()
    response = client.get("/demo/hello")
    assert response.status_code == 200
    assert response.data == b"Hello World"
