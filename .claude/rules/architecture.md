# Reglas de Arquitectura

## Clean Architecture + DDD + CQRS

Este proyecto sigue **Clean Architecture + DDD + CQRS** estrictamente.
Cada bounded context tiene exactamente 3 capas:

```
src/{context}/
├── domain/          # Reglas de negocio puras. Sin dependencias externas.
├── application/     # Casos de uso. Orquesta el dominio.
└── infrastructure/  # FastAPI, SQLAlchemy, clientes HTTP, etc.
```

El contexto `shared` contiene las abstracciones base reutilizables por todos los bounded contexts.

---

## Estructura de un Bounded Context

```
{context}/
├── domain/
│   ├── events/
│   │   └── {entidad}_{accion}.py
│   ├── exceptions/
│   │   └── {entidad}_not_found.py
│   └── models/
│       ├── entities/
│       │   └── {entidad}.py
│       ├── value_objects/
│       │   └── {vo_name}.py
│       ├── {agregado}.py
│       └── {agregado}_repository.py
├── application/
│   ├── {entities}_response.py             ← response compartido entre handlers
│   └── {accion}_{entidad}/
│       ├── {accion}_{entidad}_command.py
│       ├── {accion}_{entidad}_command_handler.py
│       ├── {accion}_{entidad}_query.py
│       ├── {accion}_{entidad}_query_handler.py
│       └── {accion}_{entidad}_response.py  ← response específico del use case
├── infrastructure/
│   ├── api/
│   │   ├── router.py
│   │   └── {accion}_{entidad}_view.py
│   ├── repositories/
│   │   └── sql_alchemy_{agregado}_repository.py
│   ├── subscribers/
│   │   └── {accion}_when_{evento}.py
│   ├── clients/
│   └── {entidad}_model.py
└── tests/
    ├── domain/
    │   ├── builders/
    │   └── {context}_unit_test_suite_case.py
    ├── application/
    │   ├── builders/
    │   └── {caso_de_uso}/
    │       ├── {command|query}_mother.py
    │       └── test_{handler}.py
    └── infrastructure/
        ├── api/
        └── clients/
```

---

## Capas y Responsabilidades

### Domain
- ✅ Solo lógica de negocio pura
- ✅ Sin dependencias externas (frameworks, librerías)
- ✅ Inmutabilidad en value objects
- ❌ NO importar de `application` ni `infrastructure`

### Application
- ✅ Orquesta entidades de dominio
- ✅ Depende de repositorios (puertos/interfaces)
- ✅ Publica domain events
- ❌ NO importar de `infrastructure`

### Infrastructure
- ✅ Implementa interfaces de dominio
- ✅ Conoce FastAPI, SQLAlchemy, frameworks
- ✅ Gestiona transacciones y sesiones
- ⚠️ NO contiene lógica de negocio

---

## CQRS

### Commands (Escritura)
- Modifican estado (crear, actualizar, eliminar)
- Retornan `None`
- Transacción gestionada por `CommandView.execute()` (no hace falta decorator en el handler)
- HTTP: POST, PUT, DELETE → `204 No Content`

### Queries (Lectura)
- Leen estado sin modificarlo
- Retornan un Response DTO
- Sin transacción
- HTTP: GET → `200 OK` + JSON

**Regla crítica:** Si un command necesita datos tras ejecutarse, el frontend debe hacer una query separada.

---

## Flujo de Datos

### Escritura
```
Request → CommandView → CommandBus → CommandHandler → Aggregate.method() → Repository.save() → 204
```

### Lectura
```
Request → QueryView → QueryBus → QueryHandler → Repository.find() → Response DTO → 200
```
