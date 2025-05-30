## README.md

# Archives Web App Backend

## Overview

This backend powers the Archives Web App, providing a robust API for managing users, courses, departments, assignments, resources, and submissions in an academic context. It is built with Django and Django REST Framework, supporting role-based access for students, lecturers, and class representatives.

## Project Architecture

### Core Components

* **Custom User System**: Extends Django's user model to support roles (student, class representative, lecturer) and profile fields.
* **Resource Management**: Handles courses, departments, assignments, resource uploads, and group-based sharing.
* **Authentication & Authorization**: Session-based authentication, role-based permissions, and secure file handling.

### App Structure

* `custom/`: User management, authentication, and custom user logic.
* `student/`: Student-specific models, views, and APIs (e.g., submissions, profile).
* `lecture/`: Lecturer-specific models, views, and APIs (e.g., assignment management).
* `resources/`: Models and APIs for courses, departments, assignments, resources, and groups.
* `app/`: Main project configuration, settings, and URL routing.

## Data Models

### User Model

* Custom user model with role-based access
* Fields: username, email, full\_name, role, etc.
* Role-specific fields for students and lecturers

### Resource Model

* Fields: id, group\_id, course\_id, assignment, resource\_type, resource\_url, resource\_file, etc.
* File handling for resource uploads
* Active/inactive status tracking

### Assignment Model

* Fields: id, group\_id, course\_id, title, description, due\_date, version, etc.
* Created/updated tracking
* Maximum score configuration

### Submission Model

* Fields: id, assignment, student, submission\_date, score, feedback, etc.
* Attempt tracking
* File checksum verification

## Frontend Integration

### Authentication Flow

1. Frontend should implement login/register forms
2. Store session token after successful authentication
3. Include session token in all subsequent requests
4. Handle role-based UI rendering based on user role

### API Integration

1. Use axios or fetch for API calls
2. Implement proper error handling
3. Handle file uploads using FormData
4. Implement proper loading states

### File Handling

1. Use proper content types for file uploads
2. Handle large file uploads with progress tracking
3. Implement proper file download handling
4. Validate file types and sizes on frontend

## Setup Instructions

### Prerequisites

* Python 3.8+
* PostgreSQL
* Virtual environment (recommended)

### Installation

1. Clone the repository
2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Configure database settings in settings.py
5. Run migrations:

   ```bash
   python manage.py migrate
   ```
6. Create superuser:

   ```bash
   python manage.py createsuperuser
   ```
7. Run development server:

   ```bash
   python manage.py runserver
   ```

### Environment Variables

* `SECRET_KEY`: Django secret key
* `DEBUG`: Debug mode (True/False)
* `DATABASE_URL`: Database connection string
* `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Security Considerations

1. All endpoints require authentication except login/register
2. File uploads are validated for type and size
3. Role-based access control for sensitive operations
4. Session-based authentication with proper security measures
5. File downloads are protected and require authentication

## Limitations

1. File size limits for uploads
2. Supported file types restrictions
3. Maximum number of submissions per assignment
4. Role-based access restrictions
5. Session timeout after inactivity

## Frontend Team Guidelines

1. Implement proper error handling for all API calls
2. Use proper loading states for async operations
3. Implement proper form validation
4. Handle file uploads with progress tracking
5. Implement proper session management
6. Follow role-based UI rendering
7. Implement proper error messages for users
8. Handle API rate limiting
9. Implement proper file download handling
10. Follow security best practices

---

## See Also

* [API Documentation](docs/api.md)
