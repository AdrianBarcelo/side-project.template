# Estilo de Código

## Formato

**Línea en blanco después de `raise` o `return`** (salvo que sea la última línea):

```python
# ✅
if not category:
    raise CategoryNotFound(id)

self._category = category

# ❌
if not category:
    raise CategoryNotFound(id)
self._category = category
```

**Sin comentarios** salvo que el WHY sea no obvio. El código debe ser autoexplicativo.

**Keyword arguments** siempre explícitos:
```python
# ✅
cache.get(key=cache_key)
# ❌
cache.get(cache_key)
```

**Early returns** para evitar nesting.

**Extraer funciones** cuando la lógica supera ~5 líneas o un nombre mejora la claridad. Un nombre descriptivo > un bloque inline.

**No usar `or` para defaults** — usar `if value is None`.

**Nombres completos y descriptivos**, sin abreviaciones:
```python
# ✅
for financial_movement in financial_movements:
# ❌
for fm in financial_movements:
```

---

## Nomenclatura

| Elemento | Convención | Ejemplo |
|---|---|---|
| Clases | PascalCase | `FinancialMovement` |
| Archivos | snake_case | `financial_movement.py` |
| Funciones/Métodos | snake_case | `update_quantity()` |
| Constantes | UPPER_SNAKE_CASE | `MAX_BUDGET` |
| Commands | sufijo `Command` | `CreateOrderCommand` |
| Queries | sufijo `Query` | `GetOrderQuery` |
| Handlers | sufijo `CommandHandler`/`QueryHandler` | `CreateOrderCommandHandler` |
| Repositorios dominio | sufijo `Repository` | `OrderRepository` |
| Repositorios infra | prefijo `SqlAlchemy` | `SqlAlchemyOrderRepository` |
| Modelos SQLAlchemy | sufijo `Model` | `OrderModel` |
| Eventos | verbo en pasado | `OrderCreated` |
| Excepciones | nombre descriptivo | `OrderNotFound` |
| Colecciones dominio | plural | `Orders` |
| Mothers | sufijo `Mother` | `OrderMother` |
| Subscribers | `{accion}_when_{evento}` | `notify_when_order_created` |

---

## Dataclasses

**Commands, Queries, Events:** `@dataclass(frozen=True, kw_only=True)`

**Value Objects:** `@dataclass(frozen=True)` (sin `kw_only`)

---

## Imports

Siempre absolutos desde la raíz del paquete:
```python
# ✅
from template.shared.domain.aggregate.aggregate_root import AggregateRoot
# ❌
from ..domain.aggregate_root import AggregateRoot
```

---

## Type Hints

Obligatorios en todas las firmas de métodos públicos (Mypy strict).

---

## Herramientas

```bash
make linting    # mypy + ruff + black --check
make me-happy   # black + ruff --fix
make test       # pytest con cobertura
```
