/**
 * Mock Data para HistorySidebar
 * Genera datos de ejemplo con variedad de temas y fechas
 */

import { ChatSession, Message } from './types';

const generateId = (): string => Math.random().toString(36).substring(2, 11);

const createMessage = (
  role: 'user' | 'assistant',
  content: string,
  timestamp: Date
): Message => ({
  id: generateId(),
  role,
  content,
  timestamp,
});


export const MOCK_CHATS: ChatSession[] = [
  // ===== HOY =====
  {
    id: generateId(),
    title: 'Optimización de Base de Datos',
    createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 horas atrás
    updatedAt: new Date(Date.now() - 2 * 60 * 60 * 1000),
    messages: [
      createMessage(
        'user',
        '¿Cómo puedo optimizar las queries en PostgreSQL?',
        new Date(Date.now() - 2 * 60 * 60 * 1000)
      ),
      createMessage(
        'assistant',
        'Excelente pregunta. Aquí hay varias estrategias: 1) Crear índices en columnas frecuentemente consultadas, 2) Usar EXPLAIN ANALYZE para analizar queries lentas, 3) Normalizar datos adecuadamente...',
        new Date(Date.now() - 1.9 * 60 * 60 * 1000)
      ),
    ],
  },

  {
    id: generateId(),
    title: 'Integración de API REST',
    createdAt: new Date(Date.now() - 5 * 60 * 60 * 1000), 
    updatedAt: new Date(Date.now() - 5 * 60 * 60 * 1000),
    messages: [
      createMessage(
        'user',
        '¿Cuál es la mejor práctica para autenticación en APIs REST?',
        new Date(Date.now() - 5 * 60 * 60 * 1000)
      ),
      createMessage(
        'assistant',
        'Los estándares modernos recomiendan usar JWT (JSON Web Tokens) cuando la API es stateless, o sesiones con cookies si el servidor maniene estado. Para mayor seguridad, usa HTTPS siempre...',
        new Date(Date.now() - 4.9 * 60 * 60 * 1000)
      ),
    ],
  },

  {
    id: generateId(),
    title: 'Debug de código Python',
    createdAt: new Date(),
    updatedAt: new Date(),
    messages: [
      createMessage(
        'user',
        'Mi script de Python está lanzando un MemoryError. ¿Cómo lo debugueo?',
        new Date()
      ),
      createMessage(
        'assistant',
        'Hay varias formas. Usa memory_profiler para identificar qué líneas consumen más memoria. También considera usar generators en lugar de listas, especialmente con datos grandes...',
        new Date(Date.now() - 30 * 60 * 1000)
      ),
    ],
  },

  // ===== AYER =====
  {
    id: generateId(),
    title: 'Receta de Pasta Carbonara',
    createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    messages: [
      createMessage(
        'user',
        '¿Cómo hago una pasta carbonara auténtica?',
        new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
      ),
      createMessage(
        'assistant',
        'Los ingredientes esenciales son huevos, queso Pecorino Romano, guanciale (panceta italiana) y pimienta negra. La clave está en la técnica: calienta la pasta y mézclala con el guanciale antes de agregar los huevos...',
        new Date(Date.now() - 24 * 60 * 60 * 1000 + 30 * 60 * 1000)
      ),
    ],
  },

  {
    id: generateId(),
    title: 'Estrategias de SEO moderno',
    createdAt: new Date(Date.now() - 1.3 * 24 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 1.3 * 24 * 60 * 60 * 1000),
    messages: [
      createMessage(
        'user',
        '¿Cuáles son las tendencias de SEO en 2026?',
        new Date(Date.now() - 1.3 * 24 * 60 * 60 * 1000)
      ),
      createMessage(
        'assistant',
        'Enfócate en Core Web Vitals, contenido de alta calidad, búsqueda por voz, experiencia de usuario y E-E-A-T (Expertise, Experiential, Authority, Trust). Google también valora cada vez más el contenido original y la relevancia...',
        new Date(Date.now() - 1.29 * 24 * 60 * 60 * 1000)
      ),
    ],
  },

  // ===== HACE 2-3 DÍAS =====
  {
    id: generateId(),
    title: 'Explicación de Mecánica Cuántica',
    createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    messages: [
      createMessage(
        'user',
        '¿Qué es la mecánica cuántica en términos simples?',
        new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
      ),
      createMessage(
        'assistant',
        'La mecánica cuántica estudia el comportamiento de la materia y la energía a escalas atómicas. A diferencia de la física clásica, los electrones y fotones pueden existir en múltiples estados simultáneamente (superposición) hasta ser observados...',
        new Date(Date.now() - 2 * 24 * 60 * 60 * 1000 + 5 * 60 * 1000)
      ),
    ],
  },

  {
    id: generateId(),
    title: 'Arquitectura de Microservicios',
    createdAt: new Date(Date.now() - 2.5 * 24 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 2.5 * 24 * 60 * 60 * 1000),
    messages: [
      createMessage(
        'user',
        '¿Cuándo debería migrar de Monolítico a Microservicios?',
        new Date(Date.now() - 2.5 * 24 * 60 * 60 * 1000)
      ),
      createMessage(
        'assistant',
        'Solo cuando tu aplicación es lo suficientemente compleja. Microservicios añaden complejidad operacional (orquestación, logging distribuido, testing). Usa monolítico modular primero, y migra cuando tengas equipos independientes...',
        new Date(Date.now() - 2.49 * 24 * 60 * 60 * 1000)
      ),
    ],
  },

  {
    id: generateId(),
    title: 'Mejores prácticas de Git',
    createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
    messages: [
      createMessage(
        'user',
        '¿Cómo debo estructurar mis commits y ramas?',
        new Date(Date.now() - 3 * 24 * 60 * 60 * 1000)
      ),
      createMessage(
        'assistant',
        'Usa Git Flow o GitHub Flow según tu proyecto. Commits atómicos con mensajes claros. Prefijo: feat/, fix/, docs/, refactor/. Ramas descriptivas. Code review antes de merge. Mantén main siempre deployable...',
        new Date(Date.now() - 3 * 24 * 60 * 60 * 1000 + 10 * 60 * 1000)
      ),
    ],
  },

  // ===== HACE 5-7 DÍAS =====
  {
    id: generateId(),
    title: 'React Hooks Avanzados',
    createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
    messages: [
      createMessage(
        'user',
        '¿Cuándo usar useCallback versus useMemo?',
        new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
      ),
      createMessage(
        'assistant',
        'useCallback memoriza funciones (útil para pasar a children), useMemo memoriza valores computacionales. Usa solo cuando optimización sea realmente necesaria (después de profiling), no por defecto...',
        new Date(Date.now() - 5 * 24 * 60 * 60 * 1000 + 15 * 60 * 1000)
      ),
    ],
  },
];
