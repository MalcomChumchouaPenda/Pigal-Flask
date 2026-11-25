import inspect
import pytest
import pigal_flask.security.abstract as pkg


def test_is_abstract_class():
    with pytest.raises(TypeError):
        pkg.AccessStore()


EXPECTED_ABSTRACT_METHODS = {
    "create_user",
    "find_user",
    "update_user",
    "delete_user",
    "create_role",
    "find_role",
    "update_role",
    "delete_role",
    "assign_role",
    "revoke_role",
    "find_user_roles",
    "grant_permission",
    "revoke_permission",
    "find_role_permissions",
}


def test_declare_expected_abstract_methods():
    methods = pkg.AccessStore.__abstractmethods__
    assert methods == EXPECTED_ABSTRACT_METHODS


@pytest.mark.parametrize(
    ("method", "parameters"),
    [
        ("create_user", ("self", "user_id", "user_pwd", "kwargs")),
        ("find_user", ("self", "user_id")),
        ("update_user", ("self", "user_id", "kwargs")),
        ("delete_user", ("self", "user_id")),
        ("create_role", ("self", "role_id", "kwargs")),
        ("find_role", ("self", "role_id")),
        ("update_role", ("self", "role_id", "kwargs")),
        ("delete_role", ("self", "role_id")),
        ("assign_role", ("self", "user_id", "role_id")),
        ("revoke_role", ("self", "user_id", "role_id")),
        ("find_user_roles", ("self", "user_id")),
        ("grant_permission", ("self", "role_id", "permission")),
        ("revoke_permission", ("self", "role_id", "permission")),
        ("find_role_permissions", ("self", "role_id")),
    ],
)
def test_method_signature(method, parameters):
    method = getattr(pkg.AccessStore, method)
    signature = inspect.signature(method)
    assert tuple(signature.parameters) == parameters
