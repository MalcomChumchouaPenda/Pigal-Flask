import os
import sys
import pytest
from functools import partial
from unittest.mock import MagicMock
from flask import Blueprint
from pigal_flask import ModuleUi


def test_is_blueprint_sub_class():
    assert issubclass(ModuleUi, Blueprint)


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
def demo_name(demo_dir):
    views_file = demo_dir / "views.py"
    views_file.touch()
    import_name = 'modules.demo.views'
    yield import_name
    sys.modules.pop(import_name, None)
    

def test_is_configured_with_import_name(demo_name):
    ui = ModuleUi(demo_name)
    assert ui.import_name == demo_name


def test_has_generated_name(demo_name):
    ui = ModuleUi(demo_name)
    assert ui.name == 'demo'


def test_has_generated_template_folder(demo_name):
    ui = ModuleUi(demo_name)
    assert ui.template_folder == 'pages'


def test_has_generated_static_paths(demo_name, modules_dir):
    ui = ModuleUi(demo_name)
    assert ui.static_url_path == '/assets'
    assert ui.static_folder == os.path.join(modules_dir, 'demo', 'assets')


@pytest.fixture
def ui(demo_name):
    """ui with mocked add_url_rule"""
    ui = ModuleUi(demo_name)
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
    

@pytest.fixture
def pages_dir(demo_dir):
    pages_dir = demo_dir / "pages"
    pages_dir.mkdir()
    return pages_dir


def test_scan_static_pages(ui, pages_dir):
    (pages_dir / 'about.html').touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/about'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('about.html', )


def test_scan_index_page(ui, pages_dir):
    (pages_dir / 'index.html').touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/'
    assert endpoint == 'show_page'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('index.html', )


def test_scan_nested_static_page(ui, pages_dir):
    blog_dir = pages_dir / "blog"
    blog_dir.mkdir(parents=True)
    (blog_dir / "post.html").touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/blog/post'
    assert endpoint == 'show_page'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('blog/post.html', )


def test_scan_nested_index_page(ui, pages_dir):
    blog_dir = pages_dir / "blog"
    blog_dir.mkdir(parents=True)
    (blog_dir / "index.html").touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/blog'
    assert endpoint == 'show_page'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('blog/index.html', )


def test_scan_dynamic_page_with_one_param(ui, pages_dir):
    blog_dir = pages_dir / "blog"
    blog_dir.mkdir(parents=True)
    (blog_dir / "[id].html").touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/blog/<id>'
    assert endpoint == 'show_page'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('blog/[id].html', )


def test_scan_dynamic_page_with_multi_param(ui, pages_dir):
    nested_dir = pages_dir / "blog" / "[year]"
    nested_dir.mkdir(parents=True)
    (nested_dir / "[slug].html").touch()
    ui.scan_pages()
    
    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == '/blog/<year>/<slug>'
    assert endpoint == 'show_page'
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ('blog/[year]/[slug].html', )


def test_scan_and_avoid_duplicated_rules(ui, pages_dir):
    (pages_dir / 'index.html').touch()
    (pages_dir / 'hello.html').touch()
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
    ui.show_page('about.html')
    render_template.assert_called_with('about.html')


def test_show_dynamic_page(ui, render_template):
    ui.show_page('[id].html', id=7)
    render_template.assert_called_with('[id].html', id=7)

