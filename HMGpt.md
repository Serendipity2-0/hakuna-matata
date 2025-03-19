Create a ChatGPT-like system called HMGpt with these core components: 1.PostgreSQL database with essential tables (conversations, messages, users) for storing chat history and user data, 2. FastAPI backend with OpenAI/Claude integration, WebSocket support for real-time chat, and message streaming capabilities - install required packages: fastapi, sqlalchemy, python-openai, psycopg2-binary, python-dotenv, 3. Next.js frontend with a clean chat interface using axios, websocket, react-query, and tailwindcss for UI components. Connect these components by: setting up database connection pool and models, configuring CORS and API routes in backend, implementing WebSocket for real-time updates, and creating a responsive chat UI with message streaming and error handling. Essential features must include: message persistence, user session management, AI model integration, real-time communication, clean chat interface with loading states, and proper error handling. Before deployment, ensure database connections are tested, API endpoints are verified, real-time messaging works, AI responses are validated, and proper logging/monitoring is set up. Configure environment variables, SSL, and production database settings for deployment.


HMGpt  core components:

1) PostgreSQL database with essential tables in 'db/schema.sql':
   - conversations (conversations.sql)
   - messages (messages.sql)
   - users (users.sql)
   Store chat history and user data

2) FastAPI backend with core files:
   - main.py (app entry point)
   - app/
     - routes/chat_routes.py (API endpoints)
     - models/db_models.py (SQLAlchemy models)
     - services/
       - chat_service.py (OpenAI/Claude integration)
       - websocket_service.py (WebSocket handling)
     - database.py (database connection)
     - config.py (environment settings)
   Install required packages: fastapi, sqlalchemy, python-openai, psycopg2-binary, python-dotenv

3) Next.js frontend with core files:
   - pages/
     - index.tsx (main chat page)
     - api/chat.ts (API routes)
   - components/
     - Chat/
       - ChatWindow.tsx (main chat interface)
       - MessageList.tsx (message display)
       - InputBox.tsx (message input)
       - ConversationList.tsx (chat history)
   - services/
     - api.ts (axios setup)
     - websocket.ts (WebSocket client)
   - styles/
     - chat.css (Tailwind styles)
   Using axios, websocket, react-query, and tailwindcss for UI components

Connect these components by:
- Database connection: backend/app/database.py
- CORS config: backend/app/main.py
- API routes: backend/app/routes/chat_routes.py
- WebSocket: backend/app/services/websocket_service.py
- Frontend API integration: frontend/services/api.ts
- Chat UI: frontend/components/Chat/ChatWindow.tsx

Essential features in respective files:
- Message persistence: backend/app/models/db_models.py
- User session: backend/app/services/auth_service.py
- AI integration: backend/app/services/chat_service.py
- Real-time communication: frontend/services/websocket.ts
- Chat interface: frontend/components/Chat/*
- Error handling: backend/app/middleware/error_handler.py

Configuration files:
- Environment: .env.example
- Database: db/config.py
- Backend: backend/app/config.py
- Frontend: frontend/next.config.js

Before deployment, ensure database connections are tested (tests/db_test.py), API endpoints are verified (tests/api_test.py), real-time messaging works (tests/websocket_test.py), AI responses are validated (tests/ai_test.py), and proper logging/monitoring is set up (backend/app/utils/logger.py). Configure environment variables, SSL, and production database settings for deployment.
