"""
Tests for game logic functions in app.py.

Some tests are expected to FAIL against the current buggy code — that is intentional.
Failing tests document bugs that need to be fixed.
"""
import pytest
import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import get_range_for_difficulty, parse_guess, check_guess, update_score


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

class TestGetRangeForDifficulty:
    def test_easy_range(self):
        low, high = get_range_for_difficulty("Easy")
        assert low == 1
        assert high == 20

    def test_normal_range(self):
        low, high = get_range_for_difficulty("Normal")
        assert low == 1
        assert high == 100

    def test_hard_range_is_harder_than_normal(self):
        """BUG: Hard is currently 1-50 which is EASIER than Normal (1-100)."""
        _, normal_high = get_range_for_difficulty("Normal")
        _, hard_high = get_range_for_difficulty("Hard")
        assert hard_high > normal_high, (
            f"Hard range (1-{hard_high}) should be larger than Normal (1-{normal_high})"
        )

    def test_unknown_difficulty_returns_default(self):
        low, high = get_range_for_difficulty("Unknown")
        assert low == 1
        assert high == 100


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

class TestParseGuess:
    def test_valid_integer(self):
        ok, value, err = parse_guess("42")
        assert ok is True
        assert value == 42
        assert err is None

    def test_empty_string(self):
        ok, value, err = parse_guess("")
        assert ok is False
        assert value is None
        assert err is not None

    def test_none_input(self):
        ok, value, err = parse_guess(None)
        assert ok is False
        assert value is None
        assert err is not None

    def test_non_numeric_string(self):
        ok, value, err = parse_guess("abc")
        assert ok is False
        assert value is None
        assert err is not None

    def test_float_string_truncates_to_int(self):
        ok, value, err = parse_guess("3.7")
        assert ok is True
        assert isinstance(value, int)
        assert value == 3

    def test_negative_number(self):
        ok, value, err = parse_guess("-5")
        assert ok is True
        assert value == -5

    def test_whitespace_only(self):
        ok, value, err = parse_guess("   ")
        assert ok is False


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

class TestCheckGuess:
    def test_correct_guess_returns_win(self):
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"

    def test_correct_guess_message(self):
        outcome, message = check_guess(50, 50)
        assert "Correct" in message or "🎉" in message

    def test_guess_too_high_outcome(self):
        outcome, message = check_guess(60, 50)
        assert outcome == "Too High"

    def test_guess_too_high_hint_says_lower(self):
        """BUG: currently says 'Go HIGHER!' when guess is too high."""
        outcome, message = check_guess(60, 50)
        assert "LOWER" in message.upper(), (
            f"When guess is too high, hint should say go lower. Got: '{message}'"
        )

    def test_guess_too_low_outcome(self):
        outcome, message = check_guess(40, 50)
        assert outcome == "Too Low"

    def test_guess_too_low_hint_says_higher(self):
        """BUG: currently says 'Go LOWER!' when guess is too low."""
        outcome, message = check_guess(40, 50)
        assert "HIGHER" in message.upper(), (
            f"When guess is too low, hint should say go higher. Got: '{message}'"
        )

    def test_returns_tuple(self):
        result = check_guess(50, 50)
        assert isinstance(result, tuple) and len(result) == 2

    def test_boundary_one_below(self):
        outcome, _ = check_guess(49, 50)
        assert outcome == "Too Low"

    def test_boundary_one_above(self):
        outcome, _ = check_guess(51, 50)
        assert outcome == "Too High"

    def test_string_secret_wins_on_match(self):
        """Even attempts pass secret as str — a correct guess should still be Win."""
        outcome, _ = check_guess(50, "50")
        assert outcome == "Win"


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

class TestUpdateScore:
    def test_win_early_gives_high_score(self):
        score = update_score(0, "Win", attempt_number=1)
        assert score > 0

    def test_win_scores_decrease_with_more_attempts(self):
        score_early = update_score(0, "Win", attempt_number=1)
        score_late = update_score(0, "Win", attempt_number=8)
        assert score_early > score_late

    def test_win_score_minimum_is_10(self):
        """Winning very late should still award at least 10 points."""
        score = update_score(0, "Win", attempt_number=100)
        assert score >= 10

    def test_too_low_reduces_score(self):
        """BUG: Too Low always deducts 5, but Too High is inconsistent (adds on even attempts)."""
        score = update_score(100, "Too Low", attempt_number=1)
        assert score == 95

    def test_too_high_on_odd_attempt_reduces_score(self):
        score = update_score(100, "Too High", attempt_number=1)
        assert score == 95

    def test_too_high_on_even_attempt_also_reduces_score(self):
        """BUG: currently ADDS 5 points on even attempts for Too High — should deduct."""
        score = update_score(100, "Too High", attempt_number=2)
        assert score == 95, (
            f"Too High should always deduct points, not reward them. Got score: {score}"
        )

    def test_unknown_outcome_unchanged_score(self):
        score = update_score(42, "Draw", attempt_number=1)
        assert score == 42
