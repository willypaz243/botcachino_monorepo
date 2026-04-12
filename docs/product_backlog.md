# Product Backlog - Proyecto Botcachino (MVP)

Este documento detalla el plan de trabajo para alcanzar el Producto Mínimo Viable (MVP) en un plazo de 6 días, utilizando una estrategia de desarrollo paralelo para 5 desarrolladores con perfiles especializados.

## 🚀 Estrategia de Desarrollo (6 Días - 5 Devs)

Para maximizar la eficiencia, cada desarrollador se encargará de un "stream" vertical basado en su experiencia:

*   **Dev 1 (Data & Seed - Fullstack):** Preparación del corpus y script de carga inicial.
*   **Dev 2 (Backend/API - Fullstack):** Extensión de modelos para vectores y endpoints CRUD/Consulta.
*   **Dev 3 (AI Specialist - Especialista IA):** Implementación del Agente, Embeddings y lógica RAG.
*   **Dev 4 (Frontend User - Fullstack):** Interfaz de Chat y Carrusel de noticias.
*   **Dev 5 (Frontend Admin & DevOps - Fullstack):** Panel de gestión de contenido y despliegue (Docker/Infra).

---

## 📋 Product Backlog

### **Stream 1: Data Seeding & Preparation**
- [ ] **Task 1.1: Corpus Preparation**: Estructurar el conjunto de datos inicial (JSON/CSV) con el formato de los modelos actuales.
- [ ] **Task 1.2: Seed Script**: Crear script de Python para insertar el corpus en la DB (usando los modelos de `news.py` e `info.py`).
- [ ] **Task 1.3: Data Validation**: Verificación de que la carga sea consistente y no duplique información.

### **Stream 2: Backend & API Expansion**
- [ ] **Task 2.1: Vector Schema Update**: Modificar modelos `News` e `Info` para incluir el campo `embedding` (tipo `vector` de `pgvector`).
- [ ] **Task 2.2: API CRUD Extension**: Asegurar que los routers existentes permitan la gestión del contenido.
- [ ] **Task 2.3: Semantic Search Endpoint**: Crear el endpoint que recibe la query, llama al especialista (*Specialist*) y retorna los resultados.

### **Stream 3: AI & Agent Core (*Specialist*)**
- [ ] **Task 3.1: Embedding Pipeline**: Implementar la lógica para convertir texto en vectores (usando `sentence-transformers` o similar).
- [ ] **Task 3.2: Vector Search Logic**: Implementar la búsqueda por similitud de coseno utilizando `pgvector` en la base de datos.
- [ ] **Task 3.3: Agentic RAG Loop**: Implementar el agente que, ante una pregunta, busca en la DB y genera una respuesta natural basada *únicamente* en el contexto recuperado.

### **Stream 4: User Interface**
- [ ] **Task 4.1: Chat Interface**: Implementar componente de chat en React/Vite con soporte para mensajes de usuario y bot.
- [ ] **Task 4.2: News Carousel**: Componente visual que consuma el endpoint de noticias y permita la navegación.
- [ ] **Task 4.3: Interactive News**: Lógica para que al seleccionar una noticia del carrusel, se envíe automáticamente al chat.

### **Stream 5: Admin Panel & DevOps**
- [ ] **Task 5.1: Admin Content Management**: Vista simple para crear/editar noticias e información manualmente.
- [ ] **Task 5.2: Dockerization**: Configurar `docker-compose.yaml` para levantar PostgreSQL (con pgvector), FastAPI y Web.
- [ ] **Task 5.3: Deployment Readiness**: Configuración de variables de entorno y limpieza de la estructura de archivos para producción.

---

**Cronograma de Ejecución (6 Días)**

| Día   | Foco                  | Meta                                                     |
| :---- | :-------------------- | :------------------------------------------------------- |
| **1** | **Setup & Schema**    | Modelos con `pgvector` definidos y DB operativa.         |
| **2** | **Data & API**        | Seed funcional y Endpoints CRUD/Consulta listos.         |
| **3** | **AI Implementation** | El especialista integra Embeddings y búsqueda semántica. |
| **4** | **UI Integration**    | El Frontend se conecta a la API y muestra el Agente.     |
| **5** | **Testing & Polish**  | Pruebas de flujo completo y corrección de errores.       |
| **6** | **MVP Delivery**      | Presentación del producto con el corpus cargado.         |
