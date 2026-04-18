# Reglas de Testing

## TDD — No Negociable

Ninguna línea de código de producción sin un test fallando primero.

1. No escribir código de producción sin un test unitario que falle
2. No escribir más test del necesario para que falle
3. No escribir más código de producción del necesario para que pase

Ciclo: **RED** → **GREEN** → **REFACTOR** (solo si aporta valor) → esperar aprobación → siguiente RED. Pedir aprobación antes de cada commit.

---

## Nomenclatura

| Elemento | Convención |
|---|---|
| Archivo de test | `test_{clase_bajo_test}.py` |
| Clase de test | `Test{ClaseBajoTest}` |
| Método de test | `test_{escenario_descriptivo}` |
| Mother | `{Clase}Mother` en `{clase}_mother.py` |

---

## Mothers — Obligatorio

**ANTES de escribir un test, crear el Mother.** Nunca crear tests sin Mothers.

Clases que necesitan Mother: Aggregates, Entities, Commands, Queries, Responses, DomainEvents, Collections, ValueObjects.

### Ubicación

| Tipo | Ubicación |
|---|---|
| Aggregates, Entities, VOs, DomainEvents | `{context}/tests/domain/builders/` |
| Commands, Queries (específicos del UC) | `{context}/tests/application/{use_case}/` |
| Commands, Queries (compartidos), Responses | `{context}/tests/application/builders/` |

### Patrón UNSET

```python
from template.constants import UNSET

class OrderMother:
    @staticmethod
    def create(
        id: AggregateId = UNSET,
        customer_id: AggregateId = UNSET,
        status: str | None = UNSET,
    ) -> Order:
        return Order(
            id=id if id is not UNSET else AggregateId.random(),
            customer_id=customer_id if customer_id is not UNSET else AggregateId.random(),
            status=status if status is not UNSET else choice(["pending", None]),
        )
```

`UNSET` ≠ `None`: `UNSET` → "usar aleatorio", `None` → "explícitamente None".

### Named constructors

**Tipo 1 — Estado semántico** (cuándo el dominio tiene variantes con significado):
```python
@classmethod
def pending(cls) -> Order:
    return cls.create(status="pending")

@classmethod
def confirmed(cls) -> Order:
    return cls.create(status="confirmed")
```

**Tipo 2 — Garantía de tipo** (cuando un campo opcional debe tener valor):
```python
@classmethod
def with_note(cls, ...) -> Order:          # garantiza note: str (no None)
    return cls.create(..., note=Utils.random_string())

@classmethod
def with_filters(cls, ...) -> GetOrdersQuery:   # garantiza filtros presentes
    return cls.create(..., category_id=AggregateId.raw_uuid())

@classmethod
def without_filters(cls) -> GetOrdersQuery:
    return cls.create(category_id=None)
```

**Regla crítica:** Nunca pre-generar variables locales en los tests para resolver `str | None`. Crear el named constructor en el Mother.

```python
# ❌
subcategory_id = AggregateId.raw_uuid()
command = UpdateOrderCommandMother.create(subcategory_id=subcategory_id)

# ✅
command = UpdateOrderCommandMother.with_subcategory()
```

**Reglas de named constructors:**
- Siempre delegan en `create()` (DRY)
- Firma explícita con todos los parámetros, nunca `**kwargs`
- Parámetros garantizados sin `| None` en el tipo

### Utilidades

| Función | Uso |
|---|---|
| `Utils.random_string()` | String aleatorio |
| `Utils.random_int(min, max)` | Entero en rango |
| `AggregateId.random()` | ID para entidades de dominio |
| `AggregateId.raw_uuid()` | UUID string para Commands/Queries/Responses |
| `choice([a, b])` | Elegir aleatoriamente (campos opcionales) |

Diferencia clave: domain usa `AggregateId.random()`, commands/queries usan `AggregateId.raw_uuid()` (string).

---

## Mocking

**Dominio (repositorios, buses):** Mockito con `strict=True`

```python
from mockito.mocking import mock
from mockito import expect, arg_that

repository = mock(config_or_spec=MyRepository, spec=MyRepository, strict=True)
expect(repository, times=1).save(arg_that(AssertAggregateRootSimilar(expected)))
```

**Dependencias externas HTTP:** `responses` + `unittest.mock`

```python
@responses.activate
def test_client(self) -> None:
    responses.add(responses.GET, "https://api.example.com/data", json={...})
    # Verificar también lo que SE ENVIÓ:
    assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
```

**Teardown automático** vía `UnitTestSuiteCase`:
- `verifyStubbedInvocationsAreUsed()` — todos los `expect()` deben ejecutarse
- `verifyNoUnwantedInteractions()` — sin llamadas inesperadas
- `unstub()` — limpia stubs

---

## UnitTestSuiteCase

### Base compartida (`shared/tests/domain/unit_test_suite_case.py`)

Proporciona mocks lazy para `event_bus`, `command_bus`, `query_bus`, `uuid_generator` y helpers comunes. Ver implementación en shared.

### Extensión por bounded context (obligatoria)

Cada bounded context crea su propia clase base con mocks de sus repositorios:

```python
class OrderUnitTestSuiteCase(UnitTestSuiteCase):
    _order_repository: Mock | None

    def setup_method(self) -> None:
        super().setup_method()
        self._order_repository = None

    def order_repository(self) -> Mock:
        if self._order_repository is None:
            self._order_repository = mock(
                config_or_spec=OrderRepository, spec=OrderRepository, strict=True
            )
        return self._order_repository

    def order_repository_should_save(self, order: Order) -> None:
        expect(self.order_repository(), times=1).save(
            arg_that(AssertAggregateRootSimilar(order))
        ).thenReturn(None)

    def order_repository_should_get(self, id: AggregateId, return_value: Order) -> None:
        expect(self.order_repository(), times=1).get(id).thenReturn(return_value)

    def order_repository_should_delete(self, id: AggregateId) -> None:
        self.repository_should_delete(repository_mock=self.order_repository(), id=id)
```

Patrón: lazy init (`None` → crear en el getter), helpers `_should_{accion}()` por operación.

---

## Tests de Handlers

Setup con fixture:

```python
class TestCreateOrderCommandHandler(OrderUnitTestSuiteCase):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self._handler = CreateOrderCommandHandler(
            repository=self.order_repository(),
            event_bus=self.event_bus(),
        )
```

### CommandHandlers (AAA)

```python
def test_creates_order(self) -> None:
    # Arrange
    command = CreateOrderCommandMother.create()
    expected = OrderMother.create(id=AggregateId(command.id))
    self.order_repository_should_save(expected)

    # Act
    self._handler.handle(command)

    # Assert implícito — teardown Mockito verifica el expect()
```

Para updates: usar `deepcopy` para capturar el estado modificado esperado antes de ejecutar.

### QueryHandlers

Retornan DTO. Assert explícito. **Construir `expected_response` con Response Mother con campos explícitos del agregado, NUNCA con `.from_domain()`** (haría el test circular):

```python
def test_get_order(self) -> None:
    query = GetOrderQueryMother.create()
    order = OrderMother.create(id=AggregateId(query.id))
    self.order_repository_should_get(id=AggregateId(query.id), return_value=order)

    # ✅ Construir expected mapeando explícitamente los campos del agregado
    expected = OrderResponseMother.create(
        id=order.id.value,
        customer_id=order.customer_id.value,
    )

    response = self._handler.handle(query)

    assert response == expected
```

---

## Tests de Views (Estrategia Dual)

### 1. Test de integración (`@pytest.mark.integration`) — solo happy path

```python
@pytest.mark.integration
def test_create_order(self, client: TestClient) -> None:
    with SessionFactory.create() as session:
        # Insertar dependencias FK PRIMERO (antes del agregado principal)
        session.add(CustomerModel.from_domain(CustomerMother.create(id=...)))
        session.add(OrderModel.from_domain(OrderMother.create(id=...)))
        session.commit()

        response = client.post("/orders/", json={...})

    assert response.status_code == 204  # Commands
    # assert response.json() == {...}   # Queries: verificar JSON completo
```

**Regla crítica:** Si el repositorio usa `JOIN` (no `LEFT JOIN`), las entidades relacionadas deben existir en BD. Investigar el repositorio antes de escribir el test.

### 2. Test unitario — verifica dispatch correcto

```python
def test_dispatches_correct_command(self, client: TestClient) -> None:
    with patch.object(DependenciesContainer, "command_bus") as mock_bus:
        client.post("/orders/", json={"id": "uuid-1", "customer_id": "uuid-2"})

    mock_bus.dispatch.assert_called_once_with(
        CreateOrderCommand(id="uuid-1", customer_id="uuid-2")
    )
```

Para endpoints con parámetros opcionales: crear un test por combinación relevante (`with_filters`, `without_filters`).

---

## Tests de Clientes HTTP

```python
@responses.activate
def test_fetches_data(self) -> None:
    responses.add(responses.GET, "https://api.example.com/data", json={"key": "value"})

    result = self._client.fetch()

    # Verificar QUÉ SE ENVIÓ (headers, body), no solo la respuesta
    assert responses.calls[0].request.headers["Authorization"] == "Bearer token"
    assert result == ExpectedResponseMother.create(key="value")
```

---

## Assertion Helpers

| Helper | Cuándo usar |
|---|---|
| `AssertAggregateRootSimilar` | Comparar aggregates/entities en `repository.save()` |
| `AssertDomainEventSimilar` | Comparar DomainEvents en `event_bus.publish()` |
| `AssertObjectSimilar` | Otros objetos complejos (casos especiales) |

Todos ignoran campos auto-generados (`_events`, `event_id`, `occurred_on`).
