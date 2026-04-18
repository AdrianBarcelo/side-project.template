from template.shared.tests.domain.assert_object_similar import AssertObjectSimilar


class AssertAggregateRootSimilar(AssertObjectSimilar):
    def __init__(self, expected, ignore_fields: list[str] | None = None) -> None:
        if ignore_fields is None:
            ignore_fields = []

        ignore_fields.extend(["_events"])
        super().__init__(expected, ignore_fields)
