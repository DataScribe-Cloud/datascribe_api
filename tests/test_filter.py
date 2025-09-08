"""Testing suite for the Filter module.

This module tests the Filter class, ensuring that all supported filter operators and serialization logic
work as expected. It covers operator overloading, named operator methods, and edge cases for serialization.
"""

import unittest

from datascribe_api.filter import Filter

AGE_30 = 30
AGE_25 = 25
SCORE_80 = 80
SCORE_90 = 90
SCORE_50 = 50
SCORE_60 = 60
AGE_18 = 18
AGE_40 = 40
AGE_50 = 50
NAME_ALICE = "Alice"


class TestFilter(unittest.TestCase):
    """Unit tests for the Filter class."""

    def test_eq(self) -> None:
        """Test equals operator (==)."""
        f = Filter("age") == AGE_30
        self.assertEqual(f.to_dict(), {"column": "age", "operator": "=", "value": AGE_30})

    def test_ne(self) -> None:
        """Test not equals operator (!=)."""
        f = Filter("age") != AGE_25
        self.assertEqual(f.to_dict(), {"column": "age", "operator": "!=", "value": AGE_25})

    def test_gt(self) -> None:
        """Test greater than operator (>)."""
        f = Filter("score") > SCORE_80
        self.assertEqual(f.to_dict(), {"column": "score", "operator": ">", "value": SCORE_80})

    def test_ge(self) -> None:
        """Test greater than or equal operator (>=)."""
        f = Filter("score") >= SCORE_90
        self.assertEqual(f.to_dict(), {"column": "score", "operator": ">=", "value": SCORE_90})

    def test_lt(self) -> None:
        """Test less than operator (<)."""
        f = Filter("score") < SCORE_50
        self.assertEqual(f.to_dict(), {"column": "score", "operator": "<", "value": SCORE_50})

    def test_le(self) -> None:
        """Test less than or equal operator (<=)."""
        f = Filter("score") <= SCORE_60
        self.assertEqual(f.to_dict(), {"column": "score", "operator": "<=", "value": SCORE_60})

    def test_in_operator(self) -> None:
        """Test IN operator."""
        f = Filter("status").in_(["active", "pending"])
        self.assertEqual(f.to_dict(), {"column": "status", "operator": "in", "value": ["active", "pending"]})

    def test_not_in_operator(self) -> None:
        """Test NOT IN operator."""
        f = Filter("status").not_in(["inactive", "banned"])
        self.assertEqual(f.to_dict(), {"column": "status", "operator": "not in", "value": ["inactive", "banned"]})

    def test_like_operator(self) -> None:
        """Test LIKE operator."""
        f = Filter("name").like("%John%")
        self.assertEqual(f.to_dict(), {"column": "name", "operator": "like", "value": "%John%"})

    def test_ilike_operator(self) -> None:
        """Test ILIKE operator."""
        f = Filter("name").ilike("%john%")
        self.assertEqual(f.to_dict(), {"column": "name", "operator": "ilike", "value": "%john%"})

    def test_is_null_operator(self) -> None:
        """Test IS NULL operator."""
        f = Filter("deleted_at").is_null()
        self.assertEqual(f.to_dict(), {"column": "deleted_at", "operator": "is null", "value": None})

    def test_is_not_null_operator(self) -> None:
        """Test IS NOT NULL operator."""
        f = Filter("deleted_at").is_not_null()
        self.assertEqual(f.to_dict(), {"column": "deleted_at", "operator": "is not null", "value": None})

    def test_serialize_dict(self) -> None:
        """Test serialization of a dict filter."""
        d = {"column": "age", "operator": ">", "value": 18}
        self.assertEqual(Filter.serialize(d), d)

    def test_serialize_single_filter(self) -> None:
        """Test serialization of a single Filter object."""
        f = Filter("age") > AGE_18
        self.assertEqual(Filter.serialize(f), {"column": "age", "operator": ">", "value": AGE_18})

    def test_serialize_list_of_filters(self) -> None:
        """Test serialization of a list of Filter objects."""
        filters = [Filter("age") > AGE_18, Filter("name") == NAME_ALICE]
        expected = [
            {"column": "age", "operator": ">", "value": AGE_18},
            {"column": "name", "operator": "=", "value": NAME_ALICE},
        ]
        self.assertEqual(Filter.serialize(filters), expected)

    def test_serialize_none(self) -> None:
        """Test serialization of None as filters."""
        self.assertIsNone(Filter.serialize(None))

    def test_serialize_invalid_type(self) -> None:
        """Test serialization raises TypeError for invalid filter type."""
        with self.assertRaises(TypeError):
            Filter.serialize(123)  # ty: ignore[invalid-argument-type]
