# Reglas de Capa Application

## Commands

- `@dataclass(frozen=True, kw_only=True)`
- Heredan de `Command` (shared)
- Tipos primitivos (str, int, float) — no Value Objects
- Nombre imperativo: `CreateOrder`, `UpdateOrder`, `DeleteOrder`

```python
@dataclass(frozen=True, kw_only=True)
class CreateOrderCommand(Command):
    id: str
    customer_id: str
    total: float
```

## Queries

- `@dataclass(frozen=True, kw_only=True)`
- Heredan de `Query` (shared)
- Tipos primitivos
- Nombre: `Get*`, `Find*`, `Search*`

```python
@dataclass(frozen=True, kw_only=True)
class GetOrderQuery(Query):
    id: str
```

## Command Handlers

- Un handler por command
- `handle(command)` → `None`
- Orquestan dominio; la lógica está en las entidades
- Publican domain events tras persistir

```python
class CreateOrderCommandHandler(CommandHandler[CreateOrderCommand]):
    def __init__(self, repository: OrderRepository, event_bus: EventBus) -> None:
        self._repository = repository
        self._event_bus = event_bus

    def handle(self, command: CreateOrderCommand) -> None:
        order = Order.create(
            id=AggregateId(command.id),
            customer_id=AggregateId(command.customer_id),
        )
        self._repository.save(order)
        self._event_bus.publish(order.pull_domain_events())
```

## Query Handlers

- Un handler por query
- `handle(query)` → Response DTO
- Sin `@transactional`; solo lectura
- Usan `ReadRepository` (no el full)

```python
class GetOrderQueryHandler(QueryHandler[GetOrderQuery, OrderResponse]):
    def __init__(self, repository: OrderReadRepository) -> None:
        self._repository = repository

    def handle(self, query: GetOrderQuery) -> OrderResponse:
        order = self._repository.get(AggregateId(query.id))
        return OrderResponse.from_domain(order)
```

## Response DTOs

- `@dataclass(frozen=True, kw_only=True)` heredando `Response` (shared)
- Solo tipos primitivos
- Factory method `from_domain()`

```python
@dataclass(frozen=True, kw_only=True)
class OrderResponse(Response):
    id: str
    customer_id: str
    total: float

    @staticmethod
    def from_domain(order: Order) -> "OrderResponse":
        return OrderResponse(
            id=order.id.value,
            customer_id=order.customer_id.value,
            total=order.total,
        )
```

## Responses compartidos

Cuando el mismo DTO lo usan múltiples handlers, vive fuera de cualquier use case:

```
{context}/application/
├── {entities}_response.py   ← compartido por varios handlers
└── get_order/
    └── get_order_response.py  ← específico de un use case
```

---

## Registro en buses

En `DependenciesContainer` (o factories):

```python
# CommandBusFactory
handlers = {
    CreateOrderCommand: CreateOrderCommandHandler(
        repository=order_repository,
        event_bus=event_bus,
    ),
}

# QueryBusFactory
query_bus.register(GetOrderQuery, GetOrderQueryHandler(repository=order_repository))
```
