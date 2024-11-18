# Hakuna Matata Development Project

A comprehensive full-stack development project featuring FastAPI backend, Next.js frontend, and AI-powered agent system.

## 🌟 Features

### Current Features
- AI-powered Code Runner Agent System
- Multiple specialized agents:
  - Web Scraper Agent
  - Analyst Agent
  - Campaign Idea Agent
  - Copywriter Agent
  - User Interface Agent
  - Snowy Writer Agent (for script generation)
  - Nikhil Raghu Agent (for financial analysis)
- FastAPI Backend Integration
- Next.js Frontend with TypeScript
- Role-Based Access Control (RBAC)
- Documentation System with MkDocs

### Upcoming Features
Referenced from:

## 🏗 Project Structure

root/
│
├── backend/
│ ├── agents/ # AI Agents
│ │ ├── coderunner.py
│ │ ├── NikhilRaghu.py
│ │ └── snowywriter.py
│ ├── patterns/ # Guidelines and patterns
│ ├── routes/ # API routes
│ └── requirements.txt
│
├── frontend/
│ ├── app/
│ ├── components/
│ ├── services/
│ └── package.json
│
└── docs/ # Documentation
├── serendipitydoc/
├── trademandoc/
└── mkdocs.yml

## 🚀 Getting Started

### Prerequisites
Referenced from:

### Backend Setup
Referenced from:

### Frontend Setup
Referenced from:

## 🤖 Agent System

The project features multiple AI agents for different purposes:

1. **CodeRunner Agent**: Analyzes documentation and generates coding plans
2. **NikhilRaghu Agent**: Handles financial analysis and reporting
3. **SnowyWriter Agent**: Generates script outlines based on research

To create new agents, follow:

## 📅 Development Schedule

Project development is scheduled from October 18 to October 31, 2024. For detailed timeline, see:
```markdown:docs/trademandoc/reports/developmentSch.MD
startLine: 1
endLine: 57
```

## 🔐 RBAC System

The project implements a comprehensive Role-Based Access Control system with:
- Department management
- Role-based permissions
- User authentication
- Access logging
- Admin dashboard

## 💻 Development Guidelines

### Commit Convention
We follow strict commit message guidelines. See:
```markdown:backend/patterns/git_commit_guidelines.md
startLine: 16
endLine: 26
```

### Coding Standards
```markdown:docs/SerendipityDoc/PromptCollections.md
startLine: 1
endLine: 3
```

## 🧪 Testing

The project includes comprehensive testing:
- Backend: pytest for API and unit testing
- Frontend: Jest for component testing
- Integration testing across all modules

## 📚 Documentation

Documentation is built using MkDocs with Material theme. To run locally:
```bash
mkdocs serve
```

For deployment:
```bash
mkdocs gh-deploy
```

## 🔑 Keyboard Shortcuts

Referenced from:
```markdown:frontend/README.md
startLine: 38
endLine: 53
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Follow our commit guidelines
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

