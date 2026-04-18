from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from fastapi import Response
from sqlalchemy.orm import Session

from template.shared.domain.bus.command.command import Command
from template.shared.infrastructure.dependencies_container import DependenciesContainer
from databases import SessionFactory

TCommand = TypeVar("TCommand", bound=Command)


class CommandView(ABC, Generic[TCommand]):
    _container: DependenciesContainer

    @abstractmethod
    def build_command(self, *args: Any, **kwargs: Any) -> TCommand:
        pass

    def execute(self, *args: Any, **kwargs: Any) -> Response:
        session: Session = SessionFactory.create()
        try:
            self._container = DependenciesContainer(session=session)
            command = self.build_command(*args, **kwargs)
            self._container.command_bus.dispatch(command)
            session.commit()

            return Response(status_code=204)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
