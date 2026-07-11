
import sys
import pytest
from functools import partial
from unittest.mock import MagicMock
from flask import Blueprint
import pigal_flask._interfaces as pkg


def test_is_flask_blueprint_sub_class():
    assert issubclass(pkg.ModuleUi, Blueprint)


@pytest.fixture
def modules_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / 'fake'
    monkeypatch.syspath_prepend(str(project_dir))
    modules_dir = project_dir / 'modules' 
    modules_dir.mkdir(parents=True)
    return modules_dir

@pytest.fixture
def demo_dir(modules_dir):
    demo_dir = modules_dir / 'demo'
    demo_dir.mkdir(parents=True)
    return demo_dir


@pytest.fixture
def pages_dir(demo_dir):
    pages_dir = demo_dir / 'pages'
    pages_dir.mkdir(parents=True)
    return pages_dir

    
@pytest.fixture
def import_name(pages_dir):
    views_file = pages_dir / "routes.py"
    views_file.touch()
    import_name = 'modules.demo.pages.routes'
    yield import_name
    sys.modules.pop(import_name, None)
    

def test_is_configured_with_import_name(import_name):
    ui = pkg.ModuleUi(import_name)
    assert ui.import_name == import_name


def test_has_generated_name(import_name):
    ui = pkg.ModuleUi(import_name)
    assert ui.name == 'demo'


def test_has_generated_template_folder(import_name):
    ui = pkg.ModuleUi(import_name)
    assert ui.template_folder == '../pages'


def test_has_generated_static_paths(import_name, modules_dir):
    ui = pkg.ModuleUi(import_name)
    assert ui.static_url_path == '../static'
    assert ui.static_folder == str(modules_dir / 'demo/static')


@pytest.fixture
def ui(import_name):
    """ui with mocked add_url_rule"""
    ui = pkg.ModuleUi(import_name)
    ui.add_url_rule = MagicMock()
    return ui


@pytest.mark.parametrize('options', [{}, {'methods': ['GET']}])
def test_route_with_view_function(ui, options):
    @ui.route("/hello", **options)
    def hello():
        pass

    ui.add_url_rule.assert_called_with('/hello', view_func=hello, **options)
    assert ui.deferred_rules == ['/hello']


def test_route_with_class_based_view(ui):
    @ui.route("/hello")
    class Hello:
        as_view = MagicMock()
    
    view_func = Hello.as_view.return_value
    Hello.as_view.assert_called_with('Hello')
    ui.add_url_rule.assert_called_with('/hello', view_func=view_func)
    assert ui.deferred_rules == ['/hello']


def test_scan_static_pages(ui, pages_dir):
    (pages_dir / 'demo').mkdir()
    (pages_dir / 'demo/about.html').touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/about'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('demo/about.html', )


def test_scan_index_page(ui, pages_dir):
    (pages_dir / 'demo').mkdir()
    (pages_dir / 'demo/index.html').touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/'
    assert endpoint == 'show_page'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('demo/index.html', )


def test_scan_nested_static_page(ui, pages_dir):
    (pages_dir / 'demo/blog').mkdir(parents=True)
    (pages_dir / "demo/blog/post.html").touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/blog/post'
    assert endpoint == 'show_page'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('demo/blog/post.html', )


def test_scan_nested_index_page(ui, pages_dir):
    (pages_dir / 'demo/blog').mkdir(parents=True)
    (pages_dir / 'demo/blog/index.html').touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/blog'
    assert endpoint == 'show_page'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('demo/blog/index.html', )


def test_scan_dynamic_page_with_one_param(ui, pages_dir):
    (pages_dir / 'demo/blog').mkdir(parents=True)
    (pages_dir / 'demo/blog/[id].html').touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/blog/<id>'
    assert endpoint == 'show_page'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('demo/blog/[id].html', )


def test_scan_dynamic_page_with_multi_param(ui, pages_dir):
    (pages_dir / 'demo/blog/[year]').mkdir(parents=True)
    (pages_dir / 'demo/blog/[year]/[slug].html').touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/blog/<year>/<slug>'
    assert endpoint == 'show_page'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('demo/blog/[year]/[slug].html', )


def test_scan_and_avoid_duplicated_rules(ui, pages_dir):
    (pages_dir / 'demo').mkdir()
    (pages_dir / 'demo/index.html').touch()
    (pages_dir / 'demo/hello.html').touch()
    ui.deferred_rules = ['/', '/hello']
    ui.scan_pages()
    ui.add_url_rule.assert_not_called()


@pytest.fixture
def render_template(monkeypatch):
    import pigal_flask._interfaces as pkg
    method = MagicMock()
    monkeypatch.setattr(pkg, 'render_template', method)
    return method


def test_show_static_page(ui, render_template):
    ui.show_page('demo/about.html')
    render_template.assert_called_with('demo/about.html')


def test_show_dynamic_page(ui, render_template):
    ui.show_page('demo/[id].html', id=7)
    render_template.assert_called_with('demo/[id].html', id=7)

