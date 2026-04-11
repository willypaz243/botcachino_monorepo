# Frontend - Botcachino

Interfaz web del proyecto Botcachino.

## Stack

- React 19
- Vite (bundler)
- Bun (gestor de paquetes)
- Plain JSX (sin TypeScript)

## Comandos

```bash
bun install      # Instalar dependencias
bun run dev      # Servidor de desarrollo (http://localhost:5173)
bun run build    # Build de producción
bun run lint     # Verificar código con ESLint
bun run preview  # Previsualizar build
```

## Estructura

```
src/
├── App.jsx       # Componente principal
├── App.css       # Estilos
├── main.jsx      # Entry point
└── index.css     # Estilos globales
```

## Linting

El proyecto usa ESLint con configuración flat. La regla `varsIgnorePattern: '^[A-Z_]'` permite variables sin usar que empiecen con mayúscula o underscore.

```bash
bun run lint  # Verificar código
```
