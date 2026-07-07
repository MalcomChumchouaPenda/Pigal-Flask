
import pytest
from flask import Flask, Blueprint
from flask.views import View
from pigal_flask.views import FileBasedView


def test_is_view():
    assert issubclass(FileBasedView, View)


def test_scan_simple_pages(tmp_path):
    location = tmp_path / "pages"
    location.mkdir()
    (location / "index.html").touch()
    (location / "about.html").touch()
    routes = FileBasedView.scan(location)

    assert len(routes) == 2
    assert routes['/'] == "index.html"
    assert routes['/about'] == "about.html"


def test_scan_pages_sub_directory_index(tmp_path):
    location = tmp_path / "pages"
    blog = location / "blog"
    blog.mkdir(parents=True)
    (blog / "index.html").touch()
    routes = FileBasedView.scan(location)
    
    assert len(routes) == 1
    assert routes["/blog"] == "blog/index.html"


def test_scan_nested_page(tmp_path):
    location = tmp_path / "pages"
    blog = location / "blog"
    blog.mkdir(parents=True)
    (blog / "post.html").touch()
    routes = FileBasedView.scan(location)
    
    assert len(routes) == 1
    assert routes["/blog/post"] == "blog/post.html"


def test_scan_deep_tree_pages(tmp_path):
    location = tmp_path / "pages"
    users = location / "admin" / "users"
    users.mkdir(parents=True)
    (users / "index.html").touch()
    routes = FileBasedView.scan(location)
    
    assert len(routes) == 1
    assert routes["/admin/users"] == "admin/users/index.html"


def test_scan_dynamic_pages(tmp_path):
    location = tmp_path / "pages"
    blog = location / "blog"
    blog.mkdir(parents=True)
    (blog / "[id].html").touch()
    routes = FileBasedView.scan(location)

    assert len(routes) == 1
    assert routes["/blog/<id>"] == "blog/[id].html"


def test_scan_pages_with_multiple_parameters(tmp_path):
    location = tmp_path / "pages"
    folder = location / "blog"
    folder.mkdir(parents=True)
    nested = folder / "[year]"
    nested.mkdir(parents=True)
    (nested / "[slug].html").touch()
    routes = FileBasedView.scan(location)
    
    assert len(routes) == 1
    assert routes["/blog/<year>/<slug>"] == "blog/[year]/[slug].html"


