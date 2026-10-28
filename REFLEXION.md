# Reflexión y Aprendizaje (REFLEXION.md)
*Hackathon INESDI · Business Intelligence × Inteligencia Artificial*
*Inspirado en la metodología Kaospilot*

---

## 1. Reflexión Individual (Sofia Montero)

### ¿Qué he aprendido hoy?
He aprendido a estructurar y desplegar una arquitectura agéntica de producción conectada a una base de datos PostgreSQL Serverless en Neon, articulando el protocolo estándar MCP (Model Context Protocol) junto a una Skill heurística de negocio para la toma de decisiones financieras en tiempo real.

### ¿Qué me llevo y cómo lo aplicaré?
Me llevo la convicción de que los sistemas de Business Intelligence modernos ya no deben limitarse a dashboards pasivos; deben integrar agentes capaces de razonar, consultar bases de datos relacionales directamente y activar planes de contingencia automatizados ante alertas tempranas.

### ¿Dónde me he bloqueado y cómo lo he afrontado?
El principal reto fue sincronizar la ingesta masiva de los 32,581 registros del dataset con los límites de conexión de PostgreSQL, así como configurar la autenticación OAuth con la CLI de Neon. Lo solucioné configurando el cliente serverless con queries por lotes y reutilizando el pooler optimizado para Neon.

### ¿Qué he aportado al equipo?
La visión de negocio enfocada en el riesgo crediticio en SaaS/Fintech, la estructuración rigurosa del pipeline de datos y la orquestación del agente con herramientas MCP y visualización de KPIs.

### ¿Qué haría diferente la próxima vez?
Implementaría una capa adicional de embeddings vectoriales (Lakebase Search / pgvector en Neon) para permitir búsqueda semántica sobre comentarios cualitativos de los analistas de riesgo crediticio.

---

## 2. Reflexión Colectiva del Equipo

### ¿Qué hemos aprendido trabajando juntos?
Que el "vibe coding" guiado con rigurosidad arquitectónica permite pasar de una idea abstracta de Business Intelligence a un sistema 100% funcional y verificable en pocas horas, siempre que se mantengan separados los roles del agente, las herramientas y la persistencia de datos.

### ¿Qué nos llevamos de esta experiencia?
La certeza de que un sistema agéntico debe tener evidencias empíricas comprobables en cada fase. Un producto sencillo, probado y respaldado por una base de datos real en la nube genera mucha más confianza que una maqueta teórica.

### ¿Dónde nos hemos bloqueado y cómo lo hemos resuelto?
Nos enfrentamos al desafío de diseñar una Skill propia que no fuera trivial. Lo resolvimos investigando métricas estándar de solvencia (DTI, historial en buró, grado crediticio) y plasmándolo en un modelo algorítmico de puntuación transparente.

### ¿Cómo hemos decidido, escuchado y cuestionado a la IA?
Utilizamos a la IA como un copiloto de desarrollo y pensamiento divergente, pero cuestionamos activamente sus propuestas iniciales para asegurar que las consultas SQL respetaran las particularidades de Neon Serverless y que el frontend respondiera exactamente a los criterios de evaluación del Hackathon.

### ¿Qué haríamos diferente si empezáramos de nuevo?
Definiríamos la suite de pruebas automatizadas antes de escribir el backend (TDD) para validar cada endpoint y herramienta MCP desde el minuto cero.

---

## 3. Tres Compromisos de Mejora

- **Vamos a mantener**: El enfoque de pruebas rigurosas con evidencias reproducibles y datos reales en bases de datos cloud.
- **Vamos a cambiar**: La tendencia a confiar en configuraciones por defecto; analizaremos siempre las opciones de escalabilidad y pooler de conexiones desde el inicio.
- **Vamos a experimentar**: Con agentes autónomos multi-rol colaborativos que negocien planes de reestructuración crediticia mediante canales de comunicación activos.
