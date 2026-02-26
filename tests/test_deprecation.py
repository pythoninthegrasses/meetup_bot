import pytest
import warnings


@pytest.mark.unit
class TestPasswordHashing:
    """Verify password hashing uses bcrypt directly, not passlib."""

    def test_get_password_hash_returns_bcrypt_hash(self):
        from main import get_password_hash

        hashed = get_password_hash("testpassword")
        assert hashed.startswith("$2b$"), f"Expected bcrypt hash prefix '$2b$', got: {hashed[:4]}"

    def test_verify_password_correct(self):
        from main import get_password_hash, verify_password

        hashed = get_password_hash("testpassword")
        assert verify_password("testpassword", hashed) is True

    def test_verify_password_incorrect(self):
        from main import get_password_hash, verify_password

        hashed = get_password_hash("testpassword")
        assert verify_password("wrongpassword", hashed) is False

    def test_no_passlib_import(self):
        """passlib should not be imported by main.py."""
        import importlib
        import sys

        # Remove cached main module to re-import fresh
        mod_name = "main"
        if mod_name in sys.modules:
            # Check the source for passlib imports
            import inspect

            source = inspect.getsource(sys.modules[mod_name])
            assert "from passlib" not in source, "main.py still imports passlib"
            assert "import passlib" not in source, "main.py still imports passlib"


@pytest.mark.unit
class TestLifespan:
    """Verify app uses lifespan context manager, not on_event."""

    def test_app_has_no_on_event_startup(self):
        """The app should not use deprecated on_event handlers."""
        import inspect
        import sys

        source = inspect.getsource(sys.modules["main"])
        assert '@app.on_event("startup")' not in source, "main.py still uses @app.on_event('startup')"
        assert "@app.on_event('startup')" not in source, "main.py still uses @app.on_event('startup')"

    def test_app_has_lifespan(self):
        """The app should have a lifespan configured."""
        from main import app

        assert app.router.lifespan_context is not None, "App should have a lifespan context manager"


@pytest.mark.unit
class TestNoDeprecationWarnings:
    """Verify no deprecation warnings from password hashing."""

    def test_password_hash_no_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from main import get_password_hash, verify_password

            hashed = get_password_hash("test")
            verify_password("test", hashed)

            deprecation_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
            crypt_warnings = [x for x in deprecation_warnings if "crypt" in str(x.message).lower()]
            assert len(crypt_warnings) == 0, f"Got crypt deprecation warnings: {crypt_warnings}"
