import difflib
import pprint
from copy import deepcopy
from enum import Enum
from typing import Any, List

pp = pprint.PrettyPrinter(indent=4)

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


def filter_ignore_fields(obj, ignore_fields, visited=None):
    if visited is None:
        visited = set()

    obj_id = id(obj)
    if obj_id in visited:
        return f"<Circular reference to {obj.__class__.__name__}>"

    visited.add(obj_id)

    try:
        d = obj.__dict__.copy()
        for key, value in d.items():
            if hasattr(value, "__dict__"):
                d[key] = filter_ignore_fields(value, ignore_fields, visited)
            elif isinstance(value, list):
                d[key] = [
                    filter_ignore_fields(item, ignore_fields, visited)
                    if hasattr(item, "__dict__")
                    else item
                    for item in value
                ]
            elif isinstance(value, dict):
                d[key] = {
                    k: filter_ignore_fields(v, ignore_fields, visited)
                    if hasattr(v, "__dict__")
                    else v
                    for k, v in value.items()
                }
        for field in ignore_fields:
            d.pop(field, None)
        return d
    finally:
        visited.remove(obj_id)


def assert_aggregate_root_similar(actual, expected, ignore_fields, context=None) -> None:
    context = context or {"visited": set()}
    _assert_objects_similar(actual, expected, ignore_fields, context)


def _assert_objects_similar(actual, expected, ignore_fields, context) -> None:
    if id(actual) in context["visited"] and id(expected) in context["visited"]:
        return

    context["visited"].add(id(actual))
    context["visited"].add(id(expected))

    assert type(actual) is type(expected), f"Types differ: {type(actual)} vs {type(expected)}"

    actual_dict = _get_object_dict(actual, ignore_fields)
    expected_dict = _get_object_dict(expected, ignore_fields)

    assert (
        actual_dict.keys() == expected_dict.keys()
    ), f"Attribute keys differ: {actual_dict.keys()} vs {expected_dict.keys()}"

    for key in actual_dict:
        _assert_values_similar(actual_dict[key], expected_dict[key], ignore_fields, context)


def _get_object_dict(obj, ignore_fields) -> None:
    if hasattr(obj, "__dict__"):
        obj_dict = obj.__dict__.copy()
        for field in ignore_fields:
            obj_dict.pop(field, None)
        return obj_dict

    return {}


def _assert_values_similar(
    actual_val: Any, expected_val: Any, ignore_fields: List[str], context: dict
) -> None:
    if isinstance(actual_val, list) and isinstance(expected_val, list):
        assert len(actual_val) == len(
            expected_val
        ), f"List lengths differ: {len(actual_val)} vs {len(expected_val)}"
        for a, e in zip(actual_val, expected_val):
            _assert_values_similar(a, e, ignore_fields, context)
    elif isinstance(actual_val, dict) and isinstance(expected_val, dict):
        assert (
            actual_val.keys() == expected_val.keys()
        ), f"Dict keys differ: {actual_val.keys()} vs {expected_val.keys()}"
        for key in actual_val:
            _assert_values_similar(actual_val[key], expected_val[key], ignore_fields, context)
    elif isinstance(actual_val, Enum) and isinstance(expected_val, Enum):
        if hasattr(actual_val, "value") and hasattr(expected_val, "value"):
            assert (
                actual_val.value == expected_val.value
            ), f"Enum values differ: {actual_val.value} vs {expected_val.value}"
        assert actual_val == expected_val, f"Enum values differ: {actual_val} vs {expected_val}"
    elif hasattr(actual_val, "__dict__") and hasattr(expected_val, "__dict__"):
        _assert_objects_similar(actual_val, expected_val, ignore_fields, context)
    else:
        assert actual_val == expected_val, f"Values differ: {actual_val} vs {expected_val}"


def colored_diff(expected_str, other_str):
    diff_lines = difflib.unified_diff(
        expected_str.splitlines(),
        other_str.splitlines(),
        fromfile="Expected",
        tofile="Actual",
        lineterm="",
    )
    colored_lines = []
    for line in diff_lines:
        if line.startswith("-"):
            colored_lines.append(GREEN + line + RESET)
        elif line.startswith("+"):
            colored_lines.append(RED + line + RESET)
        else:
            colored_lines.append(line)
    return "\n".join(colored_lines)


class AssertObjectSimilar:
    def __init__(self, expected: Any, ignore_fields: List[str]) -> None:
        self.expected = deepcopy(expected)
        self.ignore_fields = ignore_fields

    def __call__(self, other) -> bool:
        if isinstance(other, AssertObjectSimilar):
            return False

        try:
            if isinstance(self.expected, list):
                if len(other) != len(self.expected):
                    filtered_expected = [
                        filter_ignore_fields(x, self.ignore_fields) for x in self.expected
                    ]
                    filtered_other = [filter_ignore_fields(x, self.ignore_fields) for x in other]
                    expected_str = pp.pformat(filtered_expected)
                    other_str = pp.pformat(filtered_other)
                    diff = colored_diff(expected_str, other_str)
                    raise AssertionError(
                        f"Difference array len: "
                        f"Expected {len(self.expected)} but actual {len(other)}\n"
                        f"Full difference:\n{diff}"
                    )

                for i in range(len(self.expected)):
                    try:
                        assert_aggregate_root_similar(
                            other[i], self.expected[i], self.ignore_fields
                        )
                    except AssertionError as error:
                        expected_str = pp.pformat(
                            filter_ignore_fields(self.expected[i], self.ignore_fields)
                        )
                        other_str = pp.pformat(filter_ignore_fields(other[i], self.ignore_fields))
                        diff = colored_diff(expected_str, other_str)
                        class_info = f"Type: {self.expected[i].__class__.__name__}\n"
                        raise AssertionError(
                            f"Difference in {i} element:\n{class_info}{diff}"
                        ) from error

                return True
            else:
                try:
                    assert_aggregate_root_similar(other, self.expected, self.ignore_fields)
                    return True
                except AssertionError as error:
                    expected_str = pp.pformat(
                        filter_ignore_fields(self.expected, self.ignore_fields)
                    )
                    other_str = pp.pformat(filter_ignore_fields(other, self.ignore_fields))
                    diff = colored_diff(expected_str, other_str)
                    class_info = f"Type: {self.expected.__class__.__name__}\n"
                    raise AssertionError(f"\nDifference:\n{class_info}{diff}{error}") from error
        except AssertionError as error:
            print(error)
            return False

    def __repr__(self) -> str:
        return f"AggregateRootSimilar({self.expected}, ignore_fields={self.ignore_fields})"
