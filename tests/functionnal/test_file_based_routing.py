
import os
import sys
import pytest
from unittest.mock import MagicMock
from flask import Flask
from pigal_flask import ModuleUi


@pytest.fixture
def app(tmpdir):
    return Flask(__name__, 
                instance_path=tmpdir.strpath, 
                instance_relative_config=True)


@pytest.fixture
def demo_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / 'fake'
    monkeypatch.syspath_prepend(str(project_dir))
    demo_dir = project_dir / 'modules' / 'demo'
    demo_dir.mkdir(parents=True)
    return demo_dir


@pytest.fixture
def demo_name(demo_dir):
    routes_file = demo_dir / "pages/routes.py"
    routes_file.touch()
    import_name = 'modules.demo.pages.routes'
    yield import_name
    sys.modules.pop(import_name, None)


@pytest.fixture
def pages_dir(demo_dir):
    pages_dir = demo_dir / 'pages'
    contents_dir = pages_dir / 'demo'
    contents_dir.mkdir(parents=True)
    return pages_dir


@pytest.fixture
def ui(demo_name):
    return ModuleUi(demo_name)


def test_route_static_page(pages_dir, app, ui):
    page_html = '<div>Hello World</div>'
    page_file = pages_dir / 'demo/hello.html'
    page_file.write_text(page_html, encoding='utf-8')

    ui.scan_pages()
    app.register_blueprint(ui, url_prefix='/demo')
    print([rule.rule for rule in app.url_map.iter_rules()])
    client = app.test_client()
    response = client.get("/demo/hello")

    assert response.status_code == 200
    assert response.data == b'<div>Hello World</div>'


@pytest.mark.parametrize('url', ['/demo', '/demo/'])
def test_route_index_page(pages_dir, app, ui, url):
    page_html = '<div>Home</div>'
    page_file = pages_dir / 'demo/index.html'
    page_file.write_text(page_html, encoding='utf-8')

    ui.scan_pages()
    app.register_blueprint(ui, url_prefix='/demo')
    client = app.test_client()
    response = client.get(url)

    assert response.status_code == 200
    assert response.data == b'<div>Home</div>'


def test_route_nested_static_page(pages_dir, app, ui):
    page_html = '<div>Any Post</div>'
    blog_dir = pages_dir / 'demo/blog'
    blog_dir.mkdir()
    page_file = blog_dir / 'post.html'
    page_file.write_text(page_html, encoding='utf-8')

    ui.scan_pages()
    app.register_blueprint(ui, url_prefix='/demo')
    client = app.test_client()
    response = client.get("/demo/blog/post")

    assert response.status_code == 200
    assert response.data == b'<div>Any Post</div>'


def test_route_nested_index_page(pages_dir, app, ui):
    page_html = '<div>A Blog</div>'
    blog_dir = pages_dir / 'demo/blog'
    blog_dir.mkdir()
    page_file = blog_dir / 'index.html'
    page_file.write_text(page_html, encoding='utf-8')

    ui.scan_pages()
    app.register_blueprint(ui, url_prefix='/demo')
    client = app.test_client()
    response = client.get("/demo/blog")

    assert response.status_code == 200
    assert response.data == b'<div>A Blog</div>'


def test_route_dynamic_page(pages_dir, app, ui):
    page_html = '<div>A Blog {{ id }}</div>'
    blog_dir = pages_dir / 'demo/blog'
    blog_dir.mkdir()
    page_file = blog_dir / '[id].html'
    page_file.write_text(page_html, encoding='utf-8')

    ui.scan_pages()
    app.register_blueprint(ui, url_prefix='/demo')
    client = app.test_client()
    response = client.get("/demo/blog/12")

    assert response.status_code == 200
    assert response.data == b'<div>A Blog 12</div>'

