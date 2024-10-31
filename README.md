# Serendipity Documentation System

A comprehensive documentation system for the Serendipity project, built using MkDocs with Material theme.

## Overview

This repository contains the documentation for various components of the Serendipity project, including:
- Agent Creation Guidelines
- HakunaMatata Development Guide
- RBAC System Documentation
- Development Schedule

## Features

- 📚 Comprehensive development guidelines
- 🔐 RBAC (Role-Based Access Control) system documentation
- 🤖 Agent creation and integration guides
- 📅 Detailed development schedule
- 🎨 Material Design theme
- 🔍 Full-text search capability

## Project Structure


docs/
├── index.md # Documentation homepage
├── AgentCreationGuideline.md # Guide for creating new agents
├── HakunaMatataDevGuide.md # Development guidelines
├── RbacGuidelines.md # RBAC system documentation
└── developmentSch.MD # Development schedule



## Getting Started

1. **Prerequisites**
   ```bash
   pip install mkdocs mkdocs-material
   ```

2. **Local Development**
   ```bash
   mkdocs serve
   ```

3. **Build Documentation**
   ```bash
   mkdocs build
   ```

4. **Deploy to GitHub Pages**
   ```bash
   mkdocs gh-deploy
   ```

## Key Documentation Sections

### 1. Agent Creation
Step-by-step guide for creating and integrating new agents into the system. See `AgentCreationGuideline.md` for detailed instructions.

### 2. Development Guidelines
Comprehensive guide covering:
- FastAPI Backend setup
- Next.js Frontend implementation
- Testing methodologies
- CI/CD pipeline configuration
- Documentation management

### 3. RBAC System
Detailed documentation of the Role-Based Access Control system, including:
- Database schema
- Permission management
- User authentication
- Department-specific access controls

### 4. Development Schedule
Detailed timeline for project implementation from October 18 to October 31, 2024.

## Theme Configuration

The documentation uses MkDocs Material theme with the following features:
- Navigation tabs
- Integrated table of contents
- Search functionality
- Code highlighting and copying
- Content tabs

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Current Features

- Coding Agent
- Hakuna Matata Integration

## Upcoming Features

- Authentication
- Local model integrations
- 3-way chatbot

# Welcome to My Docs

This is the homepage for my documentation site.

## Project Overview

Brief description of your project.

## Quick Links

- [Agent Creation Guideline](AgentCreationGuideline.md)
- [HakunaMatata Dev Guidelines](HakunaMatataDevGuide.md)
- [Rbac Guidelines](RbacGuidelines.md)
- [Development](developmentSch.MD)


Here's a schema for the SQLite RBAC system, structured in a way that outlines how an LLM can generate the necessary features and logic based on the schema and requirements:

### RBAC Database Schema Outline

#### 1. **Departments Table**
Stores the different departments within the organization.

| Column        | Type    | Constraints     |
|---------------|---------|-----------------|
| `id`          | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| `name`        | TEXT    | UNIQUE, NOT NULL |

- **Purpose**: Identifies departments, such as *Serendipity*, *Dhoomstudios*, and *Trademan*.

#### 2. **Roles Table**
Stores the various roles that users can have within each department.

| Column        | Type    | Constraints     |
|---------------|---------|-----------------|
| `id`          | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| `name`        | TEXT    | UNIQUE, NOT NULL |

- **Purpose**: Manages roles like *Admin*, *Manager*, *Executive*, and *Public*.

#### 3. **Permissions Table**
Stores the permissions that are available for assignment to roles.

| Column        | Type    | Constraints     |
|---------------|---------|-----------------|
| `id`          | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| `name`        | TEXT    | UNIQUE, NOT NULL |

- **Purpose**: Defines permissions like *scrape*, *analyze*, *coding_outline*, *generate_copy*, etc.

#### 4. **Role Permissions Table**
Maps which permissions are available for each role within a department.

| Column           | Type    | Constraints                      |
|------------------|---------|----------------------------------|
| `department_id`  | INTEGER | FOREIGN KEY (references departments.id) |
| `role_id`        | INTEGER | FOREIGN KEY (references roles.id) |
| `permission_id`  | INTEGER | FOREIGN KEY (references permissions.id) |
| **Primary Key**  | (`department_id`, `role_id`, `permission_id`) |

- **Purpose**: Specifies the access control rules by mapping roles within departments to their allowed permissions.

#### 5. **Users Table**
Stores user information and their associated department and role.

| Column           | Type    | Constraints                          |
|------------------|---------|--------------------------------------|
| `id`             | INTEGER | PRIMARY KEY, AUTOINCREMENT          |
| `email`          | TEXT    | UNIQUE, NOT NULL                    |
| `name`           | TEXT    | NULLABLE                            |
| `department_id`  | INTEGER | FOREIGN KEY (references departments.id) |
| `role_id`        | INTEGER | FOREIGN KEY (references roles.id)   |

- **Purpose**: Holds user details and maps them to a department and a role.

### Features Outline for LLM

This outline serves as a guide for implementing various features and functionalities using the database schema. Each feature will leverage the schema to enforce and manage permissions dynamically.

#### Feature 1: **User Login and Mapping**
   - **Input**: User email and token (via Google SSO)
   - **Action**: Check if the user exists in the `users` table. If not:
     - Assign the user a default role (e.g., *Public*).
     - Associate them with a default department (e.g., *Serendipity*).
     - Insert the user into the database.
   - **Output**: Return user information and their associated permissions.

#### Feature 2: **Role Permission Check**
   - **Input**: User email, requested permission
   - **Action**:
     - Retrieve the user’s department and role.
     - Fetch the permissions allowed for this role within the department from `role_permissions`.
     - Check if the requested permission is present.
   - **Output**: Boolean indicating if the user has access.

#### Feature 3: **Automatic Role Assignment for New Users**
   - **Input**: User email during login (SSO)
   - **Action**:
     - If the email does not match any predefined users, assign the *Public* role and a default department.
   - **Output**: Insert or update the user’s information in the database.

#### Feature 4: **Admin Dashboard for Role and Permission Management**
   - **Input**: Admin credentials, new roles, or permissions
   - **Action**:
     - Admin can add, update, or remove roles and permissions.
     - Admin can assign users to roles and departments.
   - **Output**: Updated database records reflecting the changes.

#### Feature 5: **Department-Specific Access Control**
   - **Input**: User login and department context
   - **Action**: Validate that the user has access to features specific to their department by checking the `role_permissions` table.
   - **Output**: Permission granted or denied response based on the user’s role within the department.

#### Feature 6: **Logging and Auditing Access Requests**
   - **Input**: User email and accessed feature
   - **Action**: Log each access request to a logging table (if added) for audit purposes. This can also include logging unauthorized access attempts.
   - **Output**: Insert logs into a `access_logs` table (if created).




