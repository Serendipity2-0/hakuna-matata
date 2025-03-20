# User Synchronization Implementation

This implementation allows the application to take the username from the Next.js Clerk frontend component and pass it as a parameter to the backend to save it in the Users.db database.

## Features Implemented

1. **Database Schema**
   - Added conversations and messages tables to the existing Users.db database
   - Created appropriate indexes for efficient querying
   - Set up foreign key relationships between tables

2. **Backend API**
   - Created a FastAPI endpoint to receive and store user information
   - Implemented user creation and retrieval functionality
   - Added the user routes to the main FastAPI application

3. **Frontend Integration**
   - Created a UserSync component that automatically sends user data to the backend when a user is signed in
   - Added the UserSync component to the layout so it's included on every page
   - Created a Next.js API route to proxy requests to the backend
   - Added a user test page to verify the synchronization is working correctly

## How to Test

1. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

   If you encounter dependency issues:
   
   - For pydantic/pydantic-core version compatibility issues, we've updated the requirements.txt file to use flexible version constraints that let pip resolve compatible versions automatically.
   
   - To avoid SQLAlchemy compatibility issues with Python 3.13, we've implemented a direct SQLite connection using the built-in `sqlite3` module instead of SQLAlchemy.
   
   - For C extension compilation issues (like "Microsoft Visual C++ 14.0 or greater is required"), we've simplified the requirements to avoid packages that require C extensions. If you need the full functionality, you'll need to install Microsoft C++ Build Tools from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   
   If you encounter Rust compilation issues, you have three options:
   
   a) Use the provided `install_rust.py` script to install Rust:
   ```bash
   python install_rust.py
   ```
   
   b) Install Rust manually from https://rustup.rs/
   
   c) Use the alternative ASGI server (hypercorn) as described in the next step

2. **Start the Backend Server**

   If you encounter dependency issues with the existing agents (like `ModuleNotFoundError: No module named 'crawl4ai'`), you can use the simplified main.py file:

   ```bash
   cd backend
   python -m uvicorn app.main_simple:app --reload
   ```

   Otherwise, you can use the full main.py file:

   Option 1 (using uvicorn):
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

   Option 2 (alternative if you encounter Rust compilation issues):
   ```bash
   cd backend
   python -m hypercorn app.main:app --reload
   ```

3. **Start the Frontend Server**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test the User Synchronization**
   - Sign in to the application using Clerk
   - Navigate to the User Sync Test page from the sidebar
   - The page will display both the Clerk user information and the backend user information
   - Click the "Refresh Backend Data" button to fetch the latest data from the backend

## Implementation Details

### Database Schema

The implementation adds two new tables to the existing Users.db database:

1. **conversations** - Stores chat conversations
   - id (PRIMARY KEY)
   - user_id (FOREIGN KEY to users.id)
   - title
   - created_at
   - updated_at

2. **messages** - Stores individual messages within conversations
   - id (PRIMARY KEY)
   - conversation_id (FOREIGN KEY to conversations.id)
   - user_id (FOREIGN KEY to users.id)
   - content
   - role (user, assistant, or system)
   - created_at

### Backend API

The backend API provides the following endpoints:

- `POST /api/v1/users/` - Create or update a user
- `GET /api/v1/users/{user_id}` - Get user by ID

### Frontend Integration

The frontend integration includes:

- A UserSync component that automatically sends user data to the backend
- A Next.js API route to proxy requests to the backend
- A user test page to verify the synchronization is working correctly

## Future Improvements

1. Add more robust error handling
2. Implement user authentication and authorization
3. Add more user management features
4. Implement conversation and message functionality
