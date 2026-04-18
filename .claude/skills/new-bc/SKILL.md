---
name: new-bc
description: Scaffold a new bounded context following the project's Clean Architecture + DDD + CQRS structure
---

Before anything else, read `.claude/rules/architecture.md` to understand the exact structure required.

## Proceso

1. Preguntar el nombre del bounded context (ej: `order`, `customer`)
2. Preguntar el nombre del agregado raíz (ej: `Order`, `Customer`)
3. Mostrar el árbol de archivos que se generará y esperar confirmación
4. Generar todos los archivos

## Estructura a generar

```
src/{project_package}/{context}/
├── domain/
│   ├── __init__.py
│   ├── events/
│   │   └── __init__.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── {aggregate}_not_found.py
│   └── models/
│       ├── __init__.py
│       ├── entities/
│       │   └── __init__.py
│       ├── value_objects/
│       │   └── __init__.py
│       ├── {aggregate}.py
│       └── {aggregate}_repository.py
├── application/
│   └── __init__.py
├── infrastructure/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── router.py
│   ├── repositories/
│   │   └── __init__.py
│   └── {aggregate}_model.py
└── tests/
    ├── __init__.py
    ├── domain/
    │   ├── __init__.py
    │   ├── builders/
    │   │   ├── __init__.py
    │   │   └── {aggregate}_mother.py
    │   └── {context}_unit_test_suite_case.py
    ├── application/
    │   ├── __init__.py
    │   └── builders/
    │       └── __init__.py
    └── infrastructure/
        ├── __init__.py
        └── api/
            └── __init__.py
```

## Contenido de cada archivo

### `{aggregate}.py`
Agregado raíz con:
- `__init__` con campos privados
- `@property` para cada campo
- `create()` classmethod
- Herencia de `AggregateRoot`

### `{aggregate}_repository.py`
Interfaces `{Aggregate}ReadRepository` y `{Aggregate}Repository(ReadRepository)` con métodos `get()`, `find_*()`, `save()`, `delete()`.

### `{aggregate}_not_found.py`
Excepción heredando de `NotFound`.

### `{aggregate}_mother.py`
Mother con patrón UNSET para todos los campos del agregado.

### `{context}_unit_test_suite_case.py`
Clase base extendiendo `UnitTestSuiteCase` con mock del repositorio y helpers `{context}_repository_should_save()`, `_should_get()`, `_should_delete()`.

### `router.py`
`APIRouter` vacío con prefix `/{context}s`.

### `{aggregate}_model.py`
SQLAlchemy model con `__tablename__`, columnas básicas, `from_domain()` y `to_domain()`.

## Tras generar

Recordar al usuario:
1. Registrar el repositorio en `DependenciesContainer`
2. Añadir el modelo en `alembic/env.py`
3. Añadir el router en `fast_api.py`
4. Ejecutar `make migrations m="create_{context}_table"`
