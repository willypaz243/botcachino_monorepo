# Frontend

## Stack

- React 19
- TypeScript (TSX)
- Vite
- Bun

## Estructura

```
web/
├── src/
│   ├── components/
│   │   ├── molecules/       # Componentes pequeños
│   │   │   ├── MessageBubble/
│   │   │   ├── MessageInput/
│   │   │   ├── NewsCarousel/
│   │   │   └── TypingIndicator/
│   │   └── organisms/       # Componentes compuestos
│   │       ├── ChatLayout/
│   │       ├── Footer/
│   │       ├── HistorySidebar/
│   │       └── NewsSidebar/
│   ├── hooks/               # Custom hooks
│   │   ├── useChat.ts
│   │   └── useHistory.ts
│   ├── pages/
│   │   ├── LandingPage/
│   │   └── ChatPage/
│   ├── styles/
│   │   ├── global.css
│   │   ├── tokens.css
│   │   └── variables.css
│   └── types/
│       └── api.types.ts
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## Rutas

- `/` - Landing page
- `/agent` - Chat con el agente

## Comandos

```bash
cd web
bun install          # Instalar dependencias
bun run dev         # Servidor de desarrollo (puerto 5173)
bun run build       # Build de producción
bun run typecheck  # Verificar tipos TypeScript
bun run preview    # Previsualizar build
```

## Convenciones

### Componentes

- Usar **CSS Modules** (`*.module.css`)
- TypeScript con **.tsx** para componentes
- Organizar en subcarpetas con `index.ts` para exports

### Estilos

- Tokens en `src/styles/tokens.css`
- Variables en `src/styles/variables.css`
- Colores del sistema:

```
--bg-primary: #000000
--bg-secondary: #0a0a0f
--accent: #a78bfa
--text-primary: #f3f4f6
--text-secondary: #9ca3af
```

### State Management

- Usar hooks personalizados en `src/hooks/`
- `useChat` - Gestión de mensajes
- `useHistory` - Gestión de conversaciones