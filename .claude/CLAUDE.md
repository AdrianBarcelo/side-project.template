# CLAUDE.md

## ⚠️ REGLA CRÍTICA: RULES PRIMERO

**ANTES de proponer CUALQUIER cambio de código:**

1. **IDENTIFICAR** la capa afectada en la tabla de abajo
2. **LEER** el archivo de rules correspondiente en `.claude/rules/`
3. **APLICAR** exactamente lo que dice la rule
4. **NO** asumir, NO improvisar, NO usar patrones de otros proyectos

**La adherencia a rules es PRIORITARIA sobre la velocidad.**

### Rules por capa

**Siempre leer** `.claude/rules/code-style.md` y `.claude/rules/dependencies.md` antes de cualquier cambio.

| Si vas a tocar... | Leer primero |
|---|---|
| Entidades, agregados, value objects, eventos de dominio | `.claude/rules/domain.md` |
| Commands, queries, handlers, casos de uso | `.claude/rules/application.md` |
| API (endpoints, views, payloads), repositorios, migraciones | `.claude/rules/infrastructure.md` |
| Tests, Mothers, fixtures, mocks, patrones de testing | `.claude/rules/testing.md` |

**Regla de oro:** Si una tarea afecta múltiples capas, leer TODAS las rules relevantes antes de comenzar.

---

## Rules Siempre Vigentes

- **`.claude/rules/architecture.md`** → Clean Architecture + DDD + CQRS, estructura de bounded contexts
- **`.claude/rules/dependencies.md`** → Regla de dependencias crítica (infrastructure → application → domain)
- **`.claude/rules/code-style.md`** → Estilo, formato, nomenclatura
- **`.claude/rules/testing.md`** → TDD no negociable, Mockito, Mothers

---

## Stack Técnico

- **Backend:** Python 3.11+ con FastAPI
- **Base de datos:** PostgreSQL + SQLAlchemy 2.0
- **Testing:** Pytest + Mockito (dominio) + unittest.mock/responses (HTTP externo)
- **Migraciones:** Alembic
- **Desarrollo:** Docker + Make commands
- **Linting:** Ruff + Black + Mypy

---

## TDD — No Negociable

**Sin código de producción sin un test fallando primero.**

Ciclo: RED → GREEN → REFACTOR → esperar aprobación → siguiente RED

Pedir aprobación antes de cada commit.

---

## Idioma

- **Español:** documentación, comunicación, plans, convenciones
- **Inglés:** código fuente, clases, funciones, variables, commits, branches, PRs, tests

---

## Comunicación

- **SIEMPRE pedir confirmación antes de ejecutar** — presentar plan y esperar aprobación explícita
- Respuestas concisas y directas
- Preguntar todo lo necesario antes de implementar

---

## Skills Disponibles

- **`/new-bc`** — Genera el scaffolding completo de un nuevo bounded context

---

## Flujo de Trabajo

1. **Identificar tarea** → ¿Qué capa(s) afecta?
2. **Leer rules** → Abrir fichero(s) correspondiente(s) de `.claude/rules/`
3. **RED** → Escribir test fallido
4. **GREEN** → Mínimo código para pasar
5. **REFACTOR** → Solo si aporta valor
6. **Validar** → `make test` y `make linting`
7. **Commit** → Pedir aprobación

---

## Prioridades en Conflictos

1. **Seguridad y Tests** — nunca sacrificar cobertura ni introducir vulnerabilidades
2. **Arquitectura limpia** — respetar regla de dependencias estrictamente
3. **Simplicidad (YAGNI)** — no agregar complejidad innecesaria
4. **Estilo de código** — seguir rules de código
