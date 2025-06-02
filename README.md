<<<<<<< integration
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