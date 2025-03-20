# HMGpt Task Breakdown

## 1. Database Setup (SQLite)

*   **File:** `db/schema.sql` (conversations.sql, messages.sql)
*   **Task:**
    *   Define the schema for the `conversations` and `messages` tables.
    *   Ensure proper data types and relationships between tables.
    *   Create indexes for efficient querying.
    *   Link messages to Clerk user IDs instead of a local users table.
*   **Verification:**
    *   Connect to the SQLite database using a client.
    *   Execute the SQL schema and verify table creation.
    *   Insert sample data and query to validate the schema.

## 2. FastAPI Backend Setup

*   **Core Files:**
    *   `backend/app/main.py` (App entry point)
    *   `backend/app/routes/chat_routes.py` (API endpoints)
    *   `backend/app/models/db_models.py` (SQLAlchemy models)
    *   `backend/app/services/chat_service.py` (OpenAI/Claude integration)
    *   `backend/app/services/websocket_service.py` (WebSocket handling)
    *   `backend/app/database.py` (Database connection)
    *   `backend/app/config.py` (Environment settings)
    *   `backend/app/services/auth_service.py` (Clerk integration)
*   **Tasks:**
    *   **2.1 Database Connection:**
        *   Implement SQLite connection using SQLAlchemy.
        *   Define SQLAlchemy models for `conversations` and `messages`.
        *   Link messages to Clerk user IDs.
    *   **2.2 API Endpoints:**
        *   Create API endpoints for:
            *   Creating new conversations.
            *   Retrieving conversation history.
            *   Sending messages.
        *   Implement proper request validation and error handling.
    *   **2.3 WebSocket Support:**
        *   Implement WebSocket endpoints for real-time chat.
        *   Handle message streaming from AI models.
        *   Manage user connections and disconnections.
    *   **2.4 AI Model Integration:**
        *   Integrate with OpenAI/Claude API for generating chat responses.
        *   Implement message streaming for real-time updates.
        *   Handle API authentication and error handling.
    *   **2.5 Clerk Authentication Integration:**
        *   Integrate Clerk for user authentication and authorization.
        *   Implement middleware to validate Clerk session tokens.
        *   Associate chat messages with Clerk user IDs.
    *   **2.6 Configuration:**
        *   Set up environment variables for SQLite path, API keys, Clerk keys, etc.
        *   Configure CORS for allowing frontend requests.
*   **Verification:**
    *   Run the FastAPI backend using `uvicorn`.
    *   Test API endpoints using `curl` or Postman.
    *   Verify SQLite database connections and data persistence.
    *   Test WebSocket connections and message streaming.
    *   Validate AI model responses.
    *   Verify Clerk authentication integration.

## 3. Next.js Frontend Setup

*   **Core Files:**
    *   `frontend/pages/index.tsx` (Main chat page)
    *   `frontend/pages/api/chat.ts` (API routes)
    *   `frontend/components/Chat/ChatWindow.tsx` (Main chat interface)
    *   `frontend/components/Chat/MessageList.tsx` (Message display)
    *   `frontend/components/Chat/InputBox.tsx` (Message input)
    *   `frontend/components/Chat/ConversationList.tsx` (Chat history)
    *   `frontend/services/api.ts` (Axios setup)
    *   `frontend/services/websocket.ts` (WebSocket client)
    *   `frontend/styles/chat.css` (Tailwind styles)
    *   `frontend/components/Auth/ClerkProvider.tsx` (Clerk authentication)
*   **Tasks:**
    *   **3.1 Chat UI:**
        *   Create a responsive chat interface using Tailwind CSS.
        *   Implement message display with proper styling.
        *   Create an input box for sending messages.
        *   Implement a conversation list for displaying chat history.
        *   Add loading states for AI responses.
        *   Add user authentication UI components from Clerk.
    *   **3.2 API Integration:**
        *   Set up Axios for making API requests to the backend.
        *   Implement API calls for:
            *   Creating new conversations.
            *   Retrieving conversation history.
            *   Sending messages.
        *   Include Clerk authentication tokens in API requests.
        *   Handle API errors and display appropriate messages.
    *   **3.3 WebSocket Integration:**
        *   Implement WebSocket client for real-time communication.
        *   Handle message streaming from the backend.
        *   Update the chat UI with new messages in real-time.
    *   **3.4 React Query:**
        *   Use React Query for managing API data and caching.
        *   Implement proper data fetching and error handling.
*   **Verification:**
    *   Run the Next.js frontend using `npm run dev`.
    *   Verify the chat UI is responsive and displays correctly.
    *   Test API calls and data fetching.
    *   Validate WebSocket connections and real-time updates.
    *   Ensure proper error handling and display.

## 4. Connecting Components

*   **Tasks:**
    *   Configure the backend to allow requests from the frontend origin.
    *   Set up API routes in the backend to handle frontend requests.
    *   Implement WebSocket communication between the frontend and backend.
    *   Ensure data flows correctly between the database, backend, and frontend.
*   **Verification:**
    *   Test the entire system by sending messages from the frontend and verifying they are persisted in the database and displayed in real-time.

## 5. Essential Features

*   **Message Persistence:** Ensure messages are properly stored in the SQLite database.
*   **Clerk Authentication:** Implement Clerk for user authentication and authorization.
*   **AI Model Integration:** Validate AI responses and handle errors.
*   **Real-time Communication:** Verify WebSocket connections and message streaming.
*   **Clean Chat Interface:** Ensure the chat UI is responsive and user-friendly.
*   **Error Handling:** Implement proper error handling throughout the system.

## 6. Testing and Validation

*   **Tasks:**
    *   Test database connections.
    *   Verify API endpoints.
    *   Test real-time messaging.
    *   Validate AI responses.
    *   Implement logging and monitoring.

## 7. Deployment

*   **Tasks:**
    *   Configure environment variables for production.
    *   Set up SSL for secure communication.
    *   Configure SQLite for production use or consider migration path to a more robust DB if needed.
    *   Set up Clerk production environment.
    *   Deploy the backend and frontend to a production environment