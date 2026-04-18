from template.shared.tests.domain.assert_object_similar import AssertObjectSimilar


class AssertDomainEventSimilar(AssertObjectSimilar):
    def __init__(self, expected, compare_occurred_on: bool = False) -> None:
        fields_to_ignore = ["event_id"]
        if not compare_occurred_on:
            fields_to_ignore.append("occurred_on")
        super().__init__(expected, fields_to_ignore)
