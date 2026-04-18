# Reglas de Capa Domain

## Agregados

- Heredan de `AggregateRoot` (shared)
- Campos privados con `_` prefix, acceso vía `@property`
- Propiedades computadas para valores derivados (no almacenados)
- Factory method `create()` como constructor semántico
- Métodos de negocio con verbos (`update()`, `mark_as_read()`)
- Eventos de dominio con `self.record(MyEvent.from_aggregate(self))`

```python
class Order(AggregateRoot):
    def __init__(self, id: AggregateId, total: int, ...) -> None:
        self._id = id
        self._total = total

    @property
    def id(self) -> AggregateId:
        return self._id

    @property
    def is_expensive(self) -> bool:  # computada, no almacenada
        return self._total > 1000

    @classmethod
    def create(cls, id: AggregateId, ...) -> "Order":
        instance = cls(id=id, ...)
        instance.record(OrderCreated.from_aggregate(instance))
        return instance
```

## Entidades hijas

- Heredan de `Entity` (shared)
- Gestionadas exclusivamente a través del agregado raíz
- Nunca acceder a entidades hijas directamente desde fuera del agregado

## Value Objects

- `@dataclass(frozen=True)` — inmutables
- Validación en `_assert_valid()` (se llama automáticamente en `__post_init__`)
- Sin identidad; igualdad por valor
- **Comprobar `shared/` antes de crear uno custom**

### VOs disponibles en shared

| VO | Propósito |
|---|---|
| `AggregateId` | UUID v4 para IDs de entidades |
| `Date` | Fecha sin hora (`Date.today()`, `Date.from_string("2025-01-15")`) |
| `DateTime` | Fecha con hora (`DateTime.now()`) |
| `ExternalId` | IDs de sistemas externos |
| `Month` | Mes 1-12 (IntEnum) |
| `PositiveInteger` | Entero > 0 |
| `StringId` | String no vacío |

### VO custom con validación

```python
@dataclass(frozen=True)
class Email(ValueObject):
    value: str

    def _assert_valid(self) -> None:
        if "@" not in self.value:
            raise InvalidEmail(self.value)
```

### Enum VO (alternativa para enumeraciones)

Usar `StrEnum`/`IntEnum` en lugar de `ValueObject` cuando el VO es una enumeración:

```python
class OrderStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"

    def is_pending(self) -> bool:
        return self == OrderStatus.PENDING
```

### Primitivos vs VOs

Commands/Queries/Responses usan **primitivos**. Domain usa **VOs**:

```python
# Domain
Order(id=AggregateId.random(), date=Date.today())
# Command
CreateOrderCommand(id=AggregateId.raw_uuid(), date="2025-01-15")
```

## Colecciones de dominio

- Heredan de `list[T]`
- Incluyen métodos de dominio (`get_by_id()`, `filter_pending()`)

```python
class Orders(list[Order]):
    def get_by_id(self, id: AggregateId) -> Order:
        for order in self:
            if order.id == id:
                return order
        raise OrderNotFound(id.value)
```

## Repositorios (interfaces)

- Heredan de `ABC`
- Un repositorio por agregado raíz
- Naming: `get()` lanza excepción si no encuentra; `find_*()` retorna `None` o colección vacía
- Para CQRS estricto: `ReadRepository` + `Repository` con herencia

```python
class OrderReadRepository(ABC):
    @abstractmethod
    def get(self, id: AggregateId) -> Order: ...

    @abstractmethod
    def find_all(self) -> Orders: ...

class OrderRepository(OrderReadRepository, ABC):
    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def delete(self, id: AggregateId) -> None: ...
```

## Domain Events

- `@dataclass(frozen=True, kw_only=True)`
- Heredan de `DomainEvent` (shared)
- Nombre en pasado (`OrderCreated`, `OrderUpdated`)
- Solo tipos primitivos (no Value Objects)
- Factory method `from_aggregate()`

```python
@dataclass(frozen=True, kw_only=True)
class OrderCreated(DomainEvent):
    order_id: str
    customer_id: str

    @classmethod
    def aggregate_name(cls) -> str:
        return "order"

    @classmethod
    def from_aggregate(cls, order: "Order") -> Self:
        return cls(
            aggregate_id=order.id.value,
            order_id=order.id.value,
            customer_id=order.customer_id.value,
        )
```

## Excepciones de dominio

- Heredan de `DomainException` o `NotFound` (shared)
- Implementan `error_message()` o `aggregate_class_name()`
