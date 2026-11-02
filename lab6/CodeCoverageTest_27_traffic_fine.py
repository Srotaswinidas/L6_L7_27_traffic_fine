import pytest
from traffic_fine import speeding_fine, license_action, total_penalty


# ---- starter examples ----
def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0


def test_clean_record():
    assert license_action(2, False, False) == "none"


# ---- speeding_fine: execute every line ----
def test_school_zone_very_high_excess():
    assert speeding_fine(100, 40, "school") == 6000      # excess 60 -> base*3


def test_highway_zone_high_excess():
    assert speeding_fine(130, 100, "highway") == 2000    # excess 30 -> base*2


def test_city_zone_low_excess():
    assert speeding_fine(65, 60, "city") == 500          # excess 5 -> base


# ---- license_action: execute every line ----
def test_revoke_commercial():
    assert license_action(12, True, False) == "revoke"


def test_suspend_non_commercial():
    assert license_action(12, False, False) == "suspend"


def test_suspend_repeat_offender():
    assert license_action(8, False, True) == "suspend"


def test_warning():
    assert license_action(8, False, False) == "warning"


def test_notice():
    assert license_action(4, False, False) == "notice"


# ---- total_penalty: execute every line ----
def test_total_normal():
    assert total_penalty([500, 1000]) == 1500


def test_total_negative_raises():
    with pytest.raises(ValueError):
        total_penalty([500, -1])


def test_total_capped():
    assert total_penalty([6000, 6000]) == 10000
