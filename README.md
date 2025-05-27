# Archives Web App Backend Documentation

## Overview
This backend powers the Archives Web App, providing a robust API for managing users, courses, departments, assignments, resources, and submissions in an academic context. It is built with Django and Django REST Framework, supporting role-based access for students, lecturers, and class representatives.

## Project Architecture

### Core Components
- **Custom User System**: Extends Django's user model to support roles (student, class representative, lecturer) and profile fields.
- **Resource Management**: Handles courses, departments, assignments, resource uploads, and group-based sharing.
- **Authentication & Authorization**: Session-based authentication, role-based permissions, and secure file handling.

### App Structure
- `custom/`: User management, authentication, and custom user logic.
- `student/`: Student-specific models, views, and APIs (e.g., submissions, profile).
- `lecture/`: Lecturer-specific models, views, and APIs (e.g., assignment management).
- `resources/`: Models and APIs for courses, departments, assignments, resources, and groups.
- `app/`: Main project configuration, settings, and URL routing.

## API Endpoints

### Authentication
- `POST /api/auth/login/`: User login
- `POST /api/auth/register/`: Student registration
- `GET /api/auth/whoami/`: Get current user info
- `GET /api/auth/role/`: Get user role

### User Management
- `GET /api/users/`: List users (filtered by username)
- `GET /api/users/profile/`: Get user profile
- `PUT/PATCH /api/users/update/`: Update user profile
- `DELETE /api/users/delete/`: Delete user account

### Resources
- `GET /api/resources/`: List resources
- `POST /api/resources/`: Create resource (Lecturer/CR only)
- `GET /api/resources/<id>/`: Get resource details
- `PUT/PATCH /api/resources/<id>/`: Update resource (Lecturer/CR only)
- `DELETE /api/resources/<id>/`: Delete resource (Lecturer/CR only)
- `GET /api/resources/download/<id>/`: Download resource file

### Assignments
- `GET /api/assignments/`: List assignments
- `POST /api/assignments/`: Create assignment (Lecturer only)
- `GET /api/assignments/<id>/`: Get assignment details
- `PUT/PATCH /api/assignments/<id>/`: Update assignment (Lecturer only)
- `DELETE /api/assignments/<id>/`: Delete assignment (Lecturer only)

### Submissions
- `GET /api/submissions/`: List student submissions
- `POST /api/submissions/`: Create submission
- `GET /api/submissions/<id>/`: Get submission details

### Student API

#### Authentication & Session
- **Endpoint**: `GET /api/auth/session/`
- **Authentication**: Required
- **Features**: Get current session information

#### User Profile
- **Endpoint**: `GET /api/auth/whoami/`
- **Authentication**: Required
- **Features**: Get current user's profile information
- **Response Format**:
  ```json
  {
    "full_name": "string",
    "username": "string",
    "email": "string"
  }
  ```

#### Student-Specific View
- **Endpoint**: `GET /api/student/`
- **Authentication**: Required
- **Permissions**: Student role only
- **Features**: Get student-specific information and dashboard data

#### Assignment Submissions
- **Endpoint**: `GET/POST /api/submissions/`
- **Authentication**: Required
- **Permissions**: Student role only
- **Features**:
  - List all submissions for the current student
  - Create new submission
  - Filter by assignment title
  - Order by submission date
- **Request Body (POST)**:
  ```json
  {
    "assignment": "integer",
    "file": "file",
    "attempt_number": "integer (optional)"
  }
  ```
- **Response Format**:
  ```json
  {
    "id": "integer",
    "assignment": "integer",
    "student": "integer",
    "submission_date": "datetime",
    "score": "integer",
    "feedback": "string",
    "is_graded": "boolean",
    "attempt_number": "integer",
    "file_checksum": "string"
  }
  ```

#### Submission Details
- **Endpoint**: `GET /api/submissions/<id>/`
- **Authentication**: Required
- **Permissions**: Student role only
- **Features**: Get detailed information about a specific submission

#### Resource Access
- **Endpoint**: `GET /api/student/resources/`
- **Authentication**: Required
- **Permissions**: Student role only
- **Features**:
  - List all active resources available to the student
  - Filter by resource type, course name, assignment title
  - Order by upload date
- **Response Format**:
  ```json
  {
    "id": "integer",
    "resource_type": "string",
    "course_id": "string",
    "assignment": "integer",
    "resource_url": "string",
    "resource_file": "string (URL)",
    "description": "string",
    "uploaded_at": "datetime"
  }
  ```

#### Resource Download
- **Endpoint**: `GET /api/student/resources/download/<id>/`
- **Authentication**: Required
- **Permissions**: Student role only
- **Features**: Download resource file with proper access control

## Data Models

### User Model
- Custom user model with role-based access
- Fields: username, email, full_name, role, etc.
- Role-specific fields for students and lecturers

### Resource Model
- Fields: id, group_id, course_id, assignment, resource_type, resource_url, resource_file, etc.
- File handling for resource uploads
- Active/inactive status tracking

### Assignment Model
- Fields: id, group_id, course_id, title, description, due_date, version, etc.
- Created/updated tracking
- Maximum score configuration

### Submission Model
- Fields: id, assignment, student, submission_date, score, feedback, etc.
- Attempt tracking
- File checksum verification

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
- Python 3.8+
- PostgreSQL
- Virtual environment (recommended)

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
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

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

## API Response Formats and Error Handling

### Standard Response Format
All API responses follow this structure:
```json
{
    "data": {},           // Main response data
    "message": "",        // Success/error message
    "error": "",          // Error details if any
    "status": 200,        // HTTP status code
    "meta": {            // Optional metadata
        "pagination": {}, // For paginated responses
        "filters": {},    // Applied filters
        "sort": {}        // Applied sorting
    }
}
```

### Error Response Format
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": {} // Additional error details
    },
    "status": 400
}
```

### Common Error Codes
1. **Authentication Errors (401)**:
   - `INVALID_CREDENTIALS`: Wrong username/password
   - `SESSION_EXPIRED`: Session timeout
   - `INVALID_TOKEN`: Invalid authentication token

2. **Authorization Errors (403)**:
   - `INSUFFICIENT_PERMISSIONS`: Role-based access denied
   - `RESOURCE_ACCESS_DENIED`: Resource access denied
   - `OPERATION_NOT_ALLOWED`: Action not allowed for role

3. **Validation Errors (400)**:
   - `INVALID_INPUT`: Invalid request data
   - `FILE_TOO_LARGE`: File size exceeds limit
   - `INVALID_FILE_TYPE`: Unsupported file type
   - `DUPLICATE_ENTRY`: Resource already exists

4. **Resource Errors (404)**:
   - `RESOURCE_NOT_FOUND`: Requested resource not found
   - `FILE_NOT_FOUND`: Requested file not found
   - `USER_NOT_FOUND`: User not found

5. **Server Errors (500)**:
   - `INTERNAL_ERROR`: Unexpected server error
   - `DATABASE_ERROR`: Database operation failed
   - `FILE_PROCESSING_ERROR`: File processing failed

### Rate Limiting
- Standard rate limit: 100 requests per minute
- File upload limit: 10 requests per minute
- Rate limit headers included in response:
  ```
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1620000000
  ```

### Pagination
List endpoints support pagination with these parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

Response includes pagination metadata:
```json
{
    "meta": {
        "pagination": {
            "total": 100,
            "page": 1,
            "page_size": 10,
            "total_pages": 10
        }
    }
}
```

## API Capabilities and Limitations

### Resource Management
1. **File Upload Capabilities**:
   - Supports multiple file types
   - File size limits enforced
   - Automatic file type validation
   - Secure file storage with checksums
   - Progress tracking for large uploads

2. **Resource Organization**:
   - Hierarchical structure (Department > Course > Assignment)
   - Group-based resource sharing
   - Active/inactive status tracking
   - Version control for resources
   - Metadata management (type, description, upload info)

3. **Access Control**:
   - Role-based access (Student, Lecturer, Class Representative)
   - Course-level permissions
   - Group-level permissions
   - Resource-level visibility control

### Assignment System
1. **Assignment Management**:
   - Create, update, delete assignments
   - Set due dates and maximum scores
   - Version tracking
   - Active/inactive status
   - Course and group association

2. **Submission Handling**:
   - Multiple submission attempts
   - File upload support
   - Automatic attempt tracking
   - Checksum verification
   - Grading system integration

3. **Feedback System**:
   - Score assignment
   - Written feedback
   - Grading status tracking
   - Submission history

### User Management
1. **Role-Based Access**:
   - Student: View resources, submit assignments
   - Lecturer: Manage resources, create assignments, grade submissions
   - Class Representative: Limited resource management

2. **Profile Management**:
   - Basic info (name, email, username)
   - Role-specific fields
   - Department and course associations
   - Year of study (for students)
   - Title and department (for lecturers)

### API Limitations
1. **Rate Limiting**:
   - Per-user request limits
   - Concurrent request restrictions
   - File upload size limits
   - Session timeout after inactivity

2. **File Handling**:
   - Maximum file size: 10MB
   - Supported file types: PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX, ZIP, RAR
   - Maximum number of files per resource: 1
   - File name length limit: 255 characters

3. **Data Constraints**:
   - Maximum course code length: 5 characters
   - Maximum assignment title length: 200 characters
   - Maximum resource description length: 1000 characters
   - Maximum feedback length: 2000 characters

4. **Access Restrictions**:
   - Students cannot modify resources
   - Students cannot delete submissions
   - Lecturers cannot modify other lecturers' resources
   - Class representatives have limited resource management rights
