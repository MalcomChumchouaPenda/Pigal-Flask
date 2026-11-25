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
    demo_dir.mkdir(parents=True)
    return demo_dir


@pytest.fixture
def pages_dir(demo_dir):
    pages_dir = demo_dir / "pages"
    pages_dir.mkdir(parents=True)
    return pages_dir


@pytest.fixture
def import_name(pages_dir):
    views_file = pages_dir / "routes.py"
    views_file.touch()
    import_name = "modules.demo.pages.routes"
    yield import_name
    sys.modules.pop(import_name, None)


def test_is_configured_with_import_name(import_name):
    ui = pkg.Ui(import_name)
    assert ui.import_name == import_name


def test_has_generated_name(import_name):
    ui = pkg.Ui(import_name)
    assert ui.name == "demo"


def test_has_generated_template_folder(import_name):
    ui = pkg.Ui(import_name)
    assert ui.template_folder == "../pages"


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


@pytest.fixture
def ui1(import_name):
    """ui with mocked add_url_rule"""
    ui = pkg.Ui(import_name)
    ui.add_url_rule = MagicMock()
    return ui


@pytest.mark.parametrize("options", [{}, {"methods": ["GET"]}])
def test_route_with_view_function(ui1, options):
    @ui1.route("/hello", **options)
    def hello():
        pass

    ui1.add_url_rule.assert_called_with("/hello", view_func=hello, **options)
    assert ui1.deferred_rules == ["/hello"]


def test_route_with_class_based_view(ui1):
    @ui1.route("/hello")
    class Hello:
        as_view = MagicMock()

    view_func = Hello.as_view.return_value
    Hello.as_view.assert_called_with("Hello")
    ui1.add_url_rule.assert_called_with("/hello", view_func=view_func)
    assert ui1.deferred_rules == ["/hello"]


def test_scan_static_pages(ui1, pages_dir):
    (pages_dir / "demo").mkdir()
    (pages_dir / "demo/about.html").touch()
    ui1.scan_pages()

    ui1.add_url_rule.assert_called()
    rule = ui1.add_url_rule.call_args[0][0]
    view_func = ui1.add_url_rule.call_args[0][2]
    assert rule == "/about"
    assert isinstance(view_func, partial)
    assert view_func.func == ui1.show_page
    assert view_func.args == ("demo/about.html",)


def test_scan_index_page(ui1, pages_dir):
    (pages_dir / "demo").mkdir()
    (pages_dir / "demo/index.html").touch()
    ui1.scan_pages()

    ui1.add_url_rule.assert_called()
    rule = ui1.add_url_rule.call_args[0][0]
    endpoint = ui1.add_url_rule.call_args[0][1]
    view_func = ui1.add_url_rule.call_args[0][2]
    assert rule == "/"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui1.show_page
    assert view_func.args == ("demo/index.html",)


def test_scan_home_index_page(ui1, pages_dir):
    (pages_dir / "home").mkdir()
    (pages_dir / "home/index.html").touch()
    ui1.scan_pages()

    ui1.add_url_rule.assert_called()
    rule = ui1.add_url_rule.call_args[0][0]
    endpoint = ui1.add_url_rule.call_args[0][1]
    view_func = ui1.add_url_rule.call_args[0][2]
    assert rule == "/"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui1.show_page
    assert view_func.args == ("home/index.html",)


def test_scan_nested_static_page(ui1, pages_dir):
    (pages_dir / "demo/blog").mkdir(parents=True)
    (pages_dir / "demo/blog/post.html").touch()
    ui1.scan_pages()

    ui1.add_url_rule.assert_called()
    rule = ui1.add_url_rule.call_args[0][0]
    endpoint = ui1.add_url_rule.call_args[0][1]
    view_func = ui1.add_url_rule.call_args[0][2]
    assert rule == "/blog/post"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui1.show_page
    assert view_func.args == ("demo/blog/post.html",)


def test_scan_nested_index_page(ui1, pages_dir):
    (pages_dir / "demo/blog").mkdir(parents=True)
    (pages_dir / "demo/blog/index.html").touch()
    ui1.scan_pages()

    ui1.add_url_rule.assert_called()
    rule = ui1.add_url_rule.call_args[0][0]
    endpoint = ui1.add_url_rule.call_args[0][1]
    view_func = ui1.add_url_rule.call_args[0][2]
    assert rule == "/blog"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui1.show_page
    assert view_func.args == ("demo/blog/index.html",)


def test_scan_dynamic_page_with_one_param(ui1, pages_dir):
    (pages_dir / "demo/blog").mkdir(parents=True)
    (pages_dir / "demo/blog/[id].html").touch()
    ui1.scan_pages()

    ui1.add_url_rule.assert_called()
    rule = ui1.add_url_rule.call_args[0][0]
    endpoint = ui1.add_url_rule.call_args[0][1]
    view_func = ui1.add_url_rule.call_args[0][2]
    assert rule == "/blog/<id>"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui1.show_page
    assert view_func.args == ("demo/blog/[id].html",)


def test_scan_dynamic_page_with_multi_param(ui1, pages_dir):
    (pages_dir / "demo/blog/[year]").mkdir(parents=True)
    (pages_dir / "demo/blog/[year]/[slug].html").touch()
    ui1.scan_pages()

    ui1.add_url_rule.assert_called()
    rule = ui1.add_url_rule.call_args[0][0]
    endpoint = ui1.add_url_rule.call_args[0][1]
    view_func = ui1.add_url_rule.call_args[0][2]
    assert rule == "/blog/<year>/<slug>"
    assert endpoint == "show_page"
    assert isinstance(view_func, partial)
    assert view_func.func == ui1.show_page
    assert view_func.args == ("demo/blog/[year]/[slug].html",)


def test_scan_and_avoid_duplicated_rules(ui1, pages_dir):
    (pages_dir / "demo").mkdir()
    (pages_dir / "demo/index.html").touch()
    (pages_dir / "demo/hello.html").touch()
    ui1.deferred_rules = ["/", "/hello"]
    ui1.scan_pages()
    ui1.add_url_rule.assert_not_called()


def test_scan_page_with_specific_extensions(ui1, pages_dir):
    (pages_dir / "demo/blog/[id]").mkdir(parents=True)
    (pages_dir / "demo/blog/[id]/x.html").touch()
    (pages_dir / "demo/blog/[id]/y.jinja").touch()
    (pages_dir / "demo/blog/[id]/z.jinja2").touch()
    ui1.jinja_extensions = [".jinja", ".jinja2"]
    ui1.scan_pages()

    calls = ui1.add_url_rule.call_args_list
    assert len(calls) == 2
    assert calls[0][0][0] == "/blog/<id>/y"
    assert calls[1][0][0] == "/blog/<id>/z"


@pytest.fixture
def render_template(monkeypatch):
    import pigal_flask.interfaces as pkg

    method = MagicMock()
    monkeypatch.setattr(pkg, "render_template", method)
    return method


def test_show_static_page(ui1, render_template):
    ui1.show_page("demo/about.html")
    render_template.assert_called_with("demo/about.html")


def test_show_dynamic_page(ui1, render_template):
    ui1.show_page("demo/[id].html", id=7)
    render_template.assert_called_with("demo/[id].html", id=7)


def test_bind_access(ui1):
    access = MagicMock()
    ui1.bind_access(access)
    assert ui1.access is access


def test_bind_only_once(ui1):
    ui1.bind_access(MagicMock())
    with pytest.raises(RuntimeError) as exc_info:
        ui1.bind_access(MagicMock())
    err_msg = f"{ui1} has already an access"
    assert str(exc_info.value) == err_msg


def test_require_login_without_access(ui1):
    with pytest.raises(RuntimeError) as exc_info:
        ui1.require_login()
    err_msg = f"{ui1} has no access"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def ui2(ui1):
    ui1.access = MagicMock()
    return ui1


def test_require_login_by_using_access(ui2):
    decorator = MagicMock()
    ui2.access.require_login.return_value = decorator
    result = ui2.require_login()

    ui2.access.require_login.assert_called_with()
    assert result is decorator


def test_require_role_by_using_access(ui2):
    decorator = MagicMock()
    ui2.access.require_role.return_value = decorator
    result = ui2.require_role("admin")

    assert result is decorator
    ui2.access.require_role.assert_called_with("admin")


def test_require_permission_by_using_access(ui2):
    decorator = MagicMock()
    ui2.access.require_permission.return_value = decorator
    result = ui2.require_permission("users.read")

    assert result is decorator
    ui2.access.require_permission.assert_called_with("users.read")


def test_require_multiple_permissions(ui2):
    ui2.require_permission("users.read", "users.write")
    ui2.access.require_permission.assert_called_with("users.read", "users.write")
