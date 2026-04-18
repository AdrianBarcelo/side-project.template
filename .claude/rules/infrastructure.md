# Reglas de Capa Infrastructure

## Views (API)

**CommandView** — para POST/PUT/DELETE:
- Hereda de `CommandView[TCommand]` (shared)
- Implementa `build_command()` → retorna el Command
- `execute()` inicializa `self._container` **antes** de llamar a `build_command()` — se puede usar dentro de `build_command()`
- **Nunca instanciar dependencias directamente en la view** (`UUID4Generator()`, repositorios, etc.) — siempre vía `self._container`
- Retorna siempre `204 No Content`

```python
class CreateOrderView(CommandView[CreateOrderCommand]):
    def build_command(self, payload: CreateOrderPayload) -> CreateOrderCommand:
        return CreateOrderCommand(
            id=self._container.uuid_generator.generate(),  # ✅ vía container
            customer_id=payload.customer_id,
        )

router = APIRouter(prefix="/orders")

@router.post("", status_code=204)
async def create_order(payload: CreateOrderPayload) -> Response:
    return CreateOrderView().execute(payload=payload)
```

**QueryView** — para GET:
- Hereda de `QueryView[TQuery, TResponse]` (shared)
- Implementa `build_query()` → retorna la Query
- Retorna `200 OK` + JSON

## Payloads (Pydantic)

- `{Accion}{Entidad}Payload` para requests
- `{Entidad}Response` para responses de API (distintos de los Response DTOs de application)
- Validación con Pydantic `field_validator`

## Repositorios SQLAlchemy

- Implementan la interfaz de dominio
- Nombre: `SqlAlchemy{Entidad}Repository`
- Sin transacciones (gestionadas por `CommandView.execute()`)
- Mapeo dominio ↔ ORM en `from_domain()` / `to_domain()`

```python
class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, order: Order) -> None:
        self._session.merge(OrderModel.from_domain(order))

    def get(self, id: AggregateId) -> Order:
        model = self._session.query(OrderModel).filter_by(id=id.value).first()
        if not model:
            raise OrderNotFound(id.value)
        return model.to_domain()
```

## SQLAlchemy Models

- Heredan de `Base` (shared)
- Nombre tabla: snake_case plural (`orders`, `order_items`)
- ID como String (UUID)
- Índices en foreign keys y campos de búsqueda frecuente
- `created_at` y `updated_at` heredados de `Base`
- Implementan `from_domain()` y `to_domain()`

```python
class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False, index=True)
    total = Column(Numeric(10, 2), nullable=False)

    def to_domain(self) -> Order:
        return Order(
            id=AggregateId(self.id),
            customer_id=AggregateId(self.customer_id),
            total=self.total,
        )

    @staticmethod
    def from_domain(order: Order) -> "OrderModel":
        return OrderModel(
            id=order.id.value,
            customer_id=order.customer_id.value,
            total=order.total,
        )
```

## Migraciones Alembic

```bash
make migrations m="add_total_to_orders"  # Generar
make migrate                              # Aplicar
make migrations-downgrade                # Revertir último
```

- Nombres descriptivos
- Un cambio por migración
- Siempre implementar `downgrade()`
- Importar modelos en `alembic/env.py` para autogenerate

## DependenciesContainer

Instancia repositorios concretos e inyecta en los buses:

```python
class DependenciesContainer:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._order_repository = SqlAlchemyOrderRepository(session=session)

    @property
    def command_bus(self) -> CommandBus:
        return CommandBusFactory.create(
            order_repository=self._order_repository,
            event_bus=self.event_bus,
            query_bus=self.query_bus,
            uuid_generator=self.uuid_generator,
        )
```

## Subscribers (Event Handlers)

Nombre de archivo: `{accion}_when_{evento}.py`

Heredan de `InMemoryEventHandler` (shared). Se registran en `InMemoryEventBus.HANDLERS`:

```python
# infrastructure/bus/event/in_memory_event_bus.py
HANDLERS: dict[Type[DomainEvent], set[Type[EventHandler]]] = {
    OrderCreated: {SendConfirmationEmailWhenOrderCreated},
}
```

```python
# infrastructure/subscribers/send_confirmation_email_when_order_created.py
class SendConfirmationEmailWhenOrderCreated(InMemoryEventHandler[OrderCreated]):
    def get_commands(self, event: OrderCreated) -> list[Command]:
        return [SendEmailCommand(order_id=event.order_id)]
```

## Clientes HTTP externos

- Implementan una interfaz de dominio (puerto)
- Tests con `@responses.activate`
- Verificar headers y body enviados, no solo la respuesta
