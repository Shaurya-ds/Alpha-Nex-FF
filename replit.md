# Alpha Nex - Content Platform

## Overview

Alpha Nex is a comprehensive content management platform designed for user-generated content submission, AI-powered quality assurance, and a gamified reward system. Users can upload various content types (videos, audio, documents, code, images), review others' submissions, and earn XP points convertible to monetary rewards. The platform integrates sophisticated moderation and administrative controls, aiming to be a large-scale content platform.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend
- **Framework**: Flask with SQLAlchemy ORM.
- **Database**: PostgreSQL for production, SQLite for development.
- **Authentication**: Flask-Login for session management.
- **File Handling**: Werkzeug for secure uploads, including broad file type support.
- **Background Tasks**: APScheduler for automated operations.
- **AI Integration**: OpenAI GPT-4o for content analysis and duplicate detection.

### Frontend
- **Template Engine**: Jinja2 with Bootstrap 5 for responsive design.
- **Styling**: Custom CSS with a monochrome theme and Inter font family.
- **JavaScript**: Vanilla JS for interactivity.
- **Icons**: Font Awesome.

### Security Model
- **Authentication**: Email/password with secure hashing.
- **File Validation**: Whitelisted extensions, size limits, secure filenames.
- **Rate Limiting**: Daily upload quotas.
- **Content Moderation**: AI-powered detection with human review.

### Key Features
- **User Management**: Comprehensive profiles, XP tracking, strike system, role-based access (user, admin), and daily limits.
- **Content Management**: Multi-format uploads, peer review workflow, AI quality control, secure file storage.
- **Gamification**: XP point system for uploads/reviews, monetary conversion, achievement tracking.
- **Administrative Tools**: Dashboard for managing users, content, and violations.

### Data Flow Overview
- **Upload**: User upload, frontend validation, AI analysis, secure storage, peer review queue, XP reward.
- **Review**: Reviewers rate content, aggregated scoring, flagging/removal of poor content, XP rewards for reviewers, strike system for misconduct.
- **Admin**: Monitoring, payment processing, appeal handling, platform health oversight.

## External Dependencies

### Required Services
- **OpenAI API**: For GPT-4o content analysis.
- **Database**: PostgreSQL (production), SQLite (development).
- **File Storage**: Local filesystem.

### Environment Variables
- `SESSION_SECRET`: Flask session encryption.
- `DATABASE_URL`: Database connection string.
- `OPENAI_API_KEY`: OpenAI API authentication.