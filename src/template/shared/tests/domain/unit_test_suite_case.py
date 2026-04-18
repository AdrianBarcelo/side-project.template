from typing import Any

from mockito import (
    ANY,
    arg_that,
    expect,
    unstub,
    verify,
    verifyNoUnwantedInteractions,
    verifyStubbedInvocationsAreUsed,
)
from mockito.mocking import Mock, mock

from template.shared.domain.bus.command.command import Command
from template.shared.domain.bus.command.command_bus import CommandBus
from template.shared.domain.bus.event.domain_event import DomainEvent
from template.shared.domain.bus.event.event_bus import EventBus
from template.shared.domain.bus.query.query import Query
from template.shared.domain.bus.query.query_bus import QueryBus
from template.shared.domain.uuid_generator import UuidGenerator
from template.shared.tests.domain.assert_domain_event_similar import AssertDomainEventSimilar


class UnitTestSuiteCase:
    _event_bus: Mock | None
    _command_bus: Mock | None
    _query_bus: Mock | None
    _uuid_generator: Mock | None

    def setup_method(self) -> None:
        unstub()
        self._event_bus = None
        self._command_bus = None
        self._query_bus = None
        self._uuid_generator = None

    def event_bus(self) -> Mock:
        if self._event_bus is None:
            self._event_bus = mock(config_or_spec=EventBus, spec=EventBus, strict=False)

        return self._event_bus

    def command_bus(self) -> Mock:
        if self._command_bus is None:
            self._command_bus = mock(config_or_spec=CommandBus, spec=CommandBus, strict=True)
        return self._command_bus

    def query_bus(self) -> Mock:
        if self._query_bus is None:
            self._query_bus = mock(config_or_spec=QueryBus, spec=QueryBus, strict=True)
        return self._query_bus

    def uuid_generator(self) -> Mock:
        if self._uuid_generator is None:
            self._uuid_generator = mock(
                config_or_spec=UuidGenerator, spec=UuidGenerator, strict=True
            )
        return self._uuid_generator

    def event_bus_should_publish_domain_events(
        self, domain_events: list[DomainEvent], compare_occurred_on: bool = False
    ) -> None:
        expect(self.event_bus(), times=1).publish(
            arg_that(
                AssertDomainEventSimilar(domain_events, compare_occurred_on=compare_occurred_on)
            )
        )

    def event_bus_should_not_publish_domain_events(self) -> None:
        verify(self.event_bus(), times=0).publish(ANY)

    def command_bus_should_dispatch(self, command: Command) -> None:
        expect(self.command_bus(), times=1).dispatch(command)

    def command_bus_should_not_dispatch(self) -> None:
        verify(self.command_bus(), times=0).dispatch(ANY)

    def command_bus_should_raise(self, command: Command, exception: Exception) -> None:
        expect(self.command_bus(), times=1).dispatch(command).thenRaise(exception)

    def query_bus_should_dispatch(self, query: Query, return_value: Any) -> None:
        expect(self.query_bus(), times=1).dispatch(query).thenReturn(return_value)

    def query_bus_should_raise(self, query: Query, exception: Exception) -> None:
        expect(self.query_bus(), times=1).dispatch(query).thenRaise(exception)

    def repository_should_delete(self, repository_mock: Mock, id: Any) -> None:
        expect(repository_mock, times=1).delete(id).thenReturn(None)

    def repository_should_not_delete(self, repository_mock: Mock) -> None:
        verify(repository_mock, times=0).delete(ANY)

    def repository_should_not_save(self, repository_mock: Mock) -> None:
        verify(repository_mock, times=0).save(ANY)

    def uuid_generator_should_generate(self, return_values: list[str]) -> None:
        expectation = expect(self.uuid_generator(), times=len(return_values)).generate()
        for value in return_values:
            expectation = expectation.thenReturn(value)

    def teardown_method(self) -> None:
        verifyStubbedInvocationsAreUsed()
        verifyNoUnwantedInteractions()
        unstub()
