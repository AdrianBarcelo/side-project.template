El conocimiento del proyecto se organiza en cuatro tipos:

1. **Conocimiento de proyecto** (raíz CLAUDE.md) — lo que es cierto sobre el dominio de negocio en todos los módulos. Terminología, reglas de negocio transversales, invariantes que cualquier módulo podría violar. Se carga en cada sesión y debe mantenerse corto.

2. **Conocimiento de módulo** (`<bounded_context>/CLAUDE.md`) — lo que es cierto sobre la lógica de negocio de un bounded context específico. Invariantes locales, reglas que solo importan cuando se toca ese módulo. Se carga automáticamente cuando el agente trabaja en ese módulo.

3. **Flujos** (`<módulo>/flows/*.md`) — análisis en profundidad de flujos de negocio específicos. Un archivo por caso de uso. Se leen bajo demanda al trabajar en ese flujo. Si cruzan módulos, viven en `.claude/flows/` en la raíz del proyecto.

4. **Rules** (`.claude/rules/*.md`) — cómo escribimos código en este proyecto. Convenciones de testing, patrones arquitectónicos, estilo de código. Universal al proyecto, independiente del dominio de negocio.

El conocimiento del proyecto está vivo; evoluciona con el proyecto. Nunca es una réplica del código.
