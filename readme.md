# Project Name

Event: 18th Oct 2024
Description: Showed hakuna-matata demo to Snowy


Brief description of your project.

Department -- [Serendipity, Dhoom Studios, TradeMan]
Role -- [Admin, Manager, Executive]
Project -- [{Serendipity: [AccQt, HRQt], {Dhoom Studios: BrandQt}, {TradeMan: Hakuna-Matata}]
Tasks -- Each project has task list under docs/{project}/{task_name}.md. So get the list of tasks from there.
Tools -- [{Serendipity:[ReconcilationAgent], Dhoom Studios:[ScriptWriterAgent], TradeMan:[GitCommitterAgent, RepoInfoAgent]}]

Links:
- [openai agent cookbook](https://cookbook.openai.com/examples/orchestrating_agents)
- [swarm library](https://github.com/openai/swarm)
- [git guidelines](https://registerspill.thorstenball.com/p/how-i-use-git)

## Table of Contents

- [Project Name](#project-name)
  - [Table of Contents](#table-of-contents)
  - [Resources](#resources)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
    - [Backend (FastAPI)](#backend-fastapi)
    - [Frontend (Next.js)](#frontend-nextjs)
  - [API Documentation](#api-documentation)
  - [Contributing](#contributing)
  - [License](#license)
    - [Architecture](#architecture)

## Resources

- [Chatbot](https://github.com/jakobhoeg/shadcn-chat?tab=readme-ov-file)
## Features

- List key features of your project

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- Node.js 14+
- npm or yarn

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Set up the backend:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```
   cd ../frontend
   npm install  # or yarn install
   ```

## Running the Application

### Backend (FastAPI)

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

### Frontend (Next.js)

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Start the Next.js development server:
   ```
   npm run dev  # or yarn dev
   ```

   The frontend will be available at `http://localhost:3000`.

## API Documentation

FastAPI provides automatic API documentation. Once the backend is running, you can access the docs at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

### Architecture

The FastAPI backend is designed to be modular, scalable, and easy to maintain. Below is an overview of the architecture:

1. **Directory Structure**:
   - `app/`: Contains the main application code.
     - `main.py`: The entry point of the application.
     - `routers/`: Contains all the route definitions.
     - `models/`: Contains the database models.
     - `schemas/`: Contains the Pydantic models for request and response validation.
     - `services/`: Contains the business logic and service layer.
     - `core/`: Contains core configurations and utilities.
     - `tests/`: Contains unit and integration tests.

2. **Main Components**:
   - **FastAPI Application**: The core of the backend, handling HTTP requests and responses.
   - **Database**: Typically uses SQLAlchemy for ORM and database interactions.
   - **Authentication**: JWT-based authentication for secure access.
   - **Middleware**: Custom middleware for logging, error handling, etc.
   - **Dependency Injection**: Utilizes FastAPI's dependency injection for clean and testable code.

3. **Flow**:
   - **Request Handling**: Incoming requests are routed to the appropriate endpoint in the `routers/` directory.
   - **Validation**: Requests are validated using Pydantic models defined in the `schemas/` directory.
   - **Business Logic**: The `services/` directory contains the core business logic, interacting with the database and other services.
   - **Response**: After processing, a response is returned to the client, often using Pydantic models for serialization.

4. **Configuration**:
   - Environment variables and configuration files are used to manage different environments (development, testing, production).

5. **Testing**:
   - The `tests/` directory contains unit tests for individual components and integration tests for end-to-end testing.

This architecture ensures that the FastAPI backend is robust, maintainable, and scalable, making it suitable for production environments.

Frontend Design:
1. RGB for 3 sides components and gradient gray for top component
   1.1 Red Component: Execution Component
   1.2 Green Component: Discusion Component
   1.3 Blue Component: Knowledge/Planning/Architecture Component
   1.4 Grey Component: Our work output
   
2. Center stage VIBGYOR: Showcase and feedback component
   2.1 Visual component
   2.2 Audio component
   2.3 Written text component 
Agent: Telegram agent, text clipboard agent, file search agent, terminal agent, code execution agent, audio transcript agent, kannada language agent. Project init agent for all Depts.

Backend Knowledge Gaps:
1.Async concept
2. Websocket streaming
3. Api testing
4. Agentic system design
5. Authentication and Authorization. Role based access control.

Frontend Knowledge Gaps:
1. Nextjs
2. Tailwind CSS
3. Shadcn UI
4. Typescript
5. Framer Motion
6. CSR and SSR
7. Nextjs 14 app router
8. Nextjs 14 server actions
9. Playwright testing
10. Mobile development

System Admin Knowledge Gaps:
1. Linux
2. Docker
3. Coolify
4. Networking
5. DNS and CDN
6. Database administration
7. Server monitoring and alerting
8. Server backup and recovery
9. Cursor rules