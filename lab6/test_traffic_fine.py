import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

#Example test cases:
def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0

def test_clean_record():
    assert license_action(2, False, False) == "none"

#Write the rest of the test cases so that the code is 90- 100% covered.

# ---------- speeding_fine ----------
def test_speed_equal_to_limit():
    assert speeding_fine(60, 60, "city") == 0

def test_school_zone_base():
    assert speeding_fine(65, 60, "school") == 2000

def test_highway_zone_base():
    assert speeding_fine(65, 60, "highway") == 1000

def test_city_zone_base():
    assert speeding_fine(65, 60, "city") == 500

def test_unknown_zone_uses_default():
    assert speeding_fine(65, 60, "rural") == 500

def test_excess_exactly_20_is_base():
    assert speeding_fine(80, 60, "city") == 500

def test_excess_21_is_double():
    assert speeding_fine(81, 60, "city") == 1000

def test_excess_exactly_40_is_double():
    assert speeding_fine(100, 60, "city") == 1000

def test_excess_41_is_triple():
    assert speeding_fine(101, 60, "city") == 1500

def test_school_zone_triple():
    assert speeding_fine(100, 40, "school") == 6000

def test_highway_zone_double():
    assert speeding_fine(130, 100, "highway") == 2000

# ---------- license_action ----------
def test_zero_points():
    assert license_action(0, False, False) == "none"

def test_notice_lower_boundary():
    assert license_action(4, False, False) == "notice"

def test_notice_just_below_8():
    assert license_action(7, True, True) == "notice"

def test_warning_non_repeat():
    assert license_action(8, False, False) == "warning"

def test_suspend_repeat_offender():
    assert license_action(8, False, True) == "suspend"

def test_points_11_still_warning():
    assert license_action(11, True, False) == "warning"

def test_revoke_commercial():
    assert license_action(12, True, False) == "revoke"

def test_suspend_non_commercial():
    assert license_action(12, False, True) == "suspend"

def test_high_points_commercial():
    assert license_action(20, True, True) == "revoke"

# ---------- total_penalty ----------
def test_total_empty_list():
    assert total_penalty([]) == 0

def test_total_normal():
    assert total_penalty([500, 1000]) == 1500

def test_total_zero_fine_allowed():
    assert total_penalty([0]) == 0

def test_total_negative_first_raises():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([-1])

def test_total_negative_later_raises():
    with pytest.raises(ValueError):
        total_penalty([500, -1])

def test_total_exactly_10000_not_capped():
    assert total_penalty([10000]) == 10000

def test_total_over_10000_capped():
    assert total_penalty([6000, 6000]) == 10000
