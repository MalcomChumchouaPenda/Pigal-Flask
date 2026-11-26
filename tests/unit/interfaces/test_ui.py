import sys
import pytest
from functools import partial
from unittest.mock import MagicMock, sentinel
from flask import Blueprint
import pigal_flask.interfaces as pkg


def test_is_flask_blueprint_sub_class():
    assert issubclass(pkg.Ui, Blueprint)


@pytest.fixture
def modules_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / "fake"
    monkeypatch.syspath_prepend(str(project_dir))
    modules_dir = project_dir / "modules"
    modules_dir.mkdir(parents=True)
    return modules_dir


@pytest.fixture
def demo_dir(modules_dir):
    demo_dir = modules_dir / "demo"
    pages_dir = demo_dir / "templates/demo"
    pages_dir.mkdir(parents=True)
    return demo_dir


@pytest.fixture
def import_name(demo_dir):
    views_file = demo_dir / "views.py"
    views_file.touch()
    import_name = "modules.demo.views"
    yield import_name
    sys.modules.pop(import_name, None)


def test_is_configured_with_import_name(import_name):
    ui = pkg.Ui(import_name)
    assert ui.import_name == import_name


def test_has_generated_name(import_name):
    ui = pkg.Ui(import_name)
    assert ui.name == "demo"


def test_has_generated_template_folder(import_name, modules_dir):
    ui = pkg.Ui(import_name)
    assert ui.template_folder == str(modules_dir / "demo/templates")


def test_has_generated_static_paths(import_name, modules_dir):
    ui = pkg.Ui(import_name)
    assert ui.static_url_path == "../static"
    assert ui.static_folder == str(modules_dir / "demo/static")


def test_has_default_jinja_extensions(import_name):
    ui = pkg.Ui(import_name)
    assert ui.jinja_extensions == [".html", ".jinja"]


def test_can_be_configured_by_extensions(import_name):
    ui = pkg.Ui(import_name, jinja_extensions=[".j2", ".j3"])
    assert ui.jinja_extensions == [".j2", ".j3"]


def test_has_no_default_authenticator(import_name):
    ui = pkg.Ui(import_name)
    assert ui.authenticator is None


@pytest.fixture
def ui_without_url_rules(import_name):
    """ui with mocked add_url_rule"""
    ui = pkg.Ui(import_name)
    ui.add_url_rule = MagicMock()
    return ui


@pytest.mark.parametrize("options", [{}, {"methods": ["GET"]}])
def test_route_with_view_function(ui_without_url_rules, options):
    ui = ui_without_url_rules

    @ui.route("/hello", **options)
    def hello():
        pass

    ui.add_url_rule.assert_called_with("/hello", view_func=hello, **options)
    assert ui_without_url_rules.deferred_rules == ["/hello"]


def test_route_with_class_based_view(ui_without_url_rules):
    ui = ui_without_url_rules

    @ui.route("/hello")
    class Hello:
        as_view = MagicMock()

    view_func = Hello.as_view.return_value
    Hello.as_view.assert_called_with("Hello")
    ui.add_url_rule.assert_called_with("/hello", view_func=view_func)
    assert ui_without_url_rules.deferred_rules == ["/hello"]


@pytest.fixture
def pages_dir(demo_dir):
    return demo_dir / "templates"


def test_scan_static_pages(ui_without_url_rules, pages_dir):
    (pages_dir / "demo/about.html").touch()
    ui = ui_without_url_rules

    ui.scan_pages()

    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == "/about"
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ("demo/about.html",)


def test_scan_index_page(ui_without_url_rules, pages_dir):
    (pages_dir / "demo/index.html").touch()
    ui = ui_without_url_rules

    ui.scan_pages()

    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == "/"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ("demo/index.html",)


def test_scan_home_index_page(ui_without_url_rules, pages_dir):
    (pages_dir / "home").mkdir()
    (pages_dir / "home/index.html").touch()
    ui = ui_without_url_rules

    ui.scan_pages()

    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == "/"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ("home/index.html",)


def test_scan_nested_static_page(ui_without_url_rules, pages_dir):
    (pages_dir / "demo/blog").mkdir(parents=True)
    (pages_dir / "demo/blog/post.html").touch()
    ui = ui_without_url_rules

    ui.scan_pages()

    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == "/blog/post"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ("demo/blog/post.html",)


def test_scan_nested_index_page(ui_without_url_rules, pages_dir):
    (pages_dir / "demo/blog").mkdir(parents=True)
    (pages_dir / "demo/blog/index.html").touch()
    ui = ui_without_url_rules

    ui.scan_pages()

    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == "/blog"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ("demo/blog/index.html",)


def test_scan_dynamic_page_with_one_param(ui_without_url_rules, pages_dir):
    (pages_dir / "demo/blog").mkdir(parents=True)
    (pages_dir / "demo/blog/[id].html").touch()
    ui = ui_without_url_rules

    ui.scan_pages()

    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == "/blog/<id>"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ("demo/blog/[id].html",)


def test_scan_dynamic_page_with_multi_param(ui_without_url_rules, pages_dir):
    (pages_dir / "demo/blog/[year]").mkdir(parents=True)
    (pages_dir / "demo/blog/[year]/[slug].html").touch()
    ui = ui_without_url_rules

    ui.scan_pages()

    ui.add_url_rule.assert_called()
    rule = ui.add_url_rule.call_args[0][0]
    endpoint = ui.add_url_rule.call_args[0][1]
    view_func = ui.add_url_rule.call_args[0][2]
    assert rule == "/blog/<year>/<slug>"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui.show_page
    assert view_func.args == ("demo/blog/[year]/[slug].html",)


def test_scan_and_avoid_duplicated_rules(ui_without_url_rules, pages_dir):
    (pages_dir / "demo/index.html").touch()
    (pages_dir / "demo/hello.html").touch()
    ui = ui_without_url_rules
    ui_without_url_rules.deferred_rules = ["/", "/hello"]

    ui.scan_pages()

    ui.add_url_rule.assert_not_called()


def test_scan_page_with_specific_extensions(ui_without_url_rules, pages_dir):
    (pages_dir / "demo/blog/[id]").mkdir(parents=True)
    (pages_dir / "demo/blog/[id]/x.html").touch()
    (pages_dir / "demo/blog/[id]/y.jinja").touch()
    (pages_dir / "demo/blog/[id]/z.jinja2").touch()
    ui = ui_without_url_rules
    ui.jinja_extensions = [".jinja", ".jinja2"]

    ui.scan_pages()

    calls = ui.add_url_rule.call_args_list
    assert len(calls) == 2
    assert calls[0][0][0] == "/blog/<id>/y"
    assert calls[1][0][0] == "/blog/<id>/z"


@pytest.fixture
def render_template(monkeypatch):
    import pigal_flask.interfaces as pkg

    method = MagicMock()
    monkeypatch.setattr(pkg, "render_template", method)
    return method


def test_show_static_page(ui_without_url_rules, render_template):
    ui = ui_without_url_rules
    ui.show_page("demo/about.html")
    render_template.assert_called_with("demo/about.html")


def test_show_dynamic_page(ui_without_url_rules, render_template):
    ui = ui_without_url_rules
    ui.show_page("demo/[id].html", id=7)
    render_template.assert_called_with("demo/[id].html", id=7)


@pytest.fixture
def authenticator():
    return MagicMock()

@pytest.fixture
def ui_with_rbac(import_name, authenticator):
    """ui with mocked add_url_rule"""
    ui = pkg.Ui(import_name)
    ui.authenticator = authenticator
    return ui


def test_login_required_allows_authenticated_user(ui_with_rbac, authenticator):
    authenticator.is_authenticated.return_value = True
    ui = ui_with_rbac

    @ui.login_required
    def view():
        return "Hello"

    assert view() == "Hello"


def test_login_required_rejects_anonymous(ui_with_rbac, authenticator):
    authenticator.is_authenticated.return_value = False
    authenticator.on_unauthenticated.return_value = "Login please"
    ui = ui_with_rbac

    @ui.login_required
    def view():
        return "Hello"

    assert view() == "Login please"

def test_roles_accepted_allows_authorized_user(ui_with_rbac, authenticator):
    authenticator.is_authenticated.return_value = True
    authenticator.has_roles.return_value = True
    authenticator.on_unauthorized.return_value = "No permission"
    ui = ui_with_rbac

    @ui.roles_accepted("admin")
    def view():
        return "Hi"

    assert view() == "Hi"


def test_roles_accepted_rejects_missing_role(ui_with_rbac, authenticator):
    authenticator.is_authenticated.return_value = True
    authenticator.has_roles.return_value = False
    authenticator.on_unauthorized.return_value = "No permission"
    ui = ui_with_rbac

    @ui.roles_accepted("admin")
    def view():
        return "Hi"

    assert view() == "No permission"

def test_roles_accepted_rejects_anonymous(ui_with_rbac, authenticator):
    authenticator.is_authenticated.return_value = False
    authenticator.on_unauthenticated.return_value = "Login please"
    ui = ui_with_rbac

    @ui.roles_accepted("admin")
    def view():
        return "Hi"

    assert view() == "Login please"

