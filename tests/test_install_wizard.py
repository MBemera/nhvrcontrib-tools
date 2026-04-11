from nhvr_mcp.install_wizard import module_is_available


def test_module_is_available_returns_false_for_missing_dotted_module() -> None:
    assert module_is_available("definitely_missing.module") is False
