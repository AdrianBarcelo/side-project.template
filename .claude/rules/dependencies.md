# Regla de Dependencias

Esta es la regla **MÁS CRÍTICA** del proyecto. Violarla rompe la arquitectura limpia.

## Flujo permitido

```
infrastructure → application → domain
```

| Capa | Puede importar de | NO puede importar de |
|---|---|---|
| **domain** | Solo stdlib Python | `application`, `infrastructure` |
| **application** | `domain`, `shared` | `infrastructure` |
| **infrastructure** | `domain`, `application`, frameworks | — |

## Excepción válida

Application puede importar Queries de otro bounded context para validaciones:

```python
# ✅ OK: application orquesta casos de uso entre contextos
from other_context.application.get_something.get_something_query import GetSomethingQuery
```

## Inversión de dependencias

1. **Domain** define la interfaz (`MyRepository(ABC)`)
2. **Infrastructure** implementa la interfaz (`SqlAlchemyMyRepository(MyRepository)`)
3. **Application** depende de la interfaz, no la implementación
4. **Infrastructure** inyecta la implementación vía `DependenciesContainer`
