"""Tests to verify knowledge base data is well-formed."""

from nhvrcontrib.knowledge import (
    ACCREDITATION_INFO,
    BREACH_CATEGORIES,
    COR_DUTIES,
    DIMENSION_LIMITS,
    FATIGUE_RULES,
    HML_INFO,
    MASS_LIMITS,
    PERMIT_TYPES,
    SPEED_LIMITS,
)


def test_fatigue_rules_has_all_schemes():
    assert "standard" in FATIGUE_RULES
    assert "bfm" in FATIGUE_RULES
    assert "afm" in FATIGUE_RULES
    for scheme in FATIGUE_RULES.values():
        assert "summary" in scheme


def test_mass_limits_has_general_and_hml():
    assert "general" in MASS_LIMITS
    assert "hml" in MASS_LIMITS
    assert "summary" in MASS_LIMITS["general"]
    assert "summary" in MASS_LIMITS["hml"]


def test_dimension_limits_has_key_dimensions():
    assert "height" in DIMENSION_LIMITS
    assert "width" in DIMENSION_LIMITS
    assert "length" in DIMENSION_LIMITS


def test_breach_categories_has_types():
    assert "mass" in BREACH_CATEGORIES
    assert "fatigue" in BREACH_CATEGORIES
    assert "categories" in BREACH_CATEGORIES


def test_speed_limits_not_placeholder():
    assert "default" in SPEED_LIMITS
    assert isinstance(SPEED_LIMITS["default"], dict)


def test_cor_duties_has_roles():
    assert "primary_duty" in COR_DUTIES
    assert "driver" in COR_DUTIES
    assert "operator" in COR_DUTIES


def test_accreditation_info_has_modules():
    assert "mass" in ACCREDITATION_INFO
    assert "maintenance" in ACCREDITATION_INFO
    assert "fatigue" in ACCREDITATION_INFO


def test_permit_types_has_entries():
    assert "hml" in PERMIT_TYPES
    assert "oversize" in PERMIT_TYPES


def test_hml_info_has_data():
    assert "eligibility" in HML_INFO
    assert "limits" in HML_INFO
