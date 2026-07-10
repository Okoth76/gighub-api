# GigHub Nairobi Freelance Gigs API

A FastAPI-powered backend platform matching Nairobi's top tech talent with clients. This project provides full CRUD functionalities, data validation, pagination, and advanced search criteria for freelance assignments.

## Student Information
- **Admission Number:** C027-01-1234/2026 ## Project Structure
- `main.py` - The complete FastAPI application code, Pydantic data schemas, and backend route logic.
- `README.md` - Documentation overview.

## Core Features
- **Pydantic Validation:** Stricter constraint validation on pricing models and project workflow tracking.
- **Search Engine:** Keyphrase scanning over titles and descriptive logs with specialized categories filtering.
- **Pagination Slicing:** Safe listing utilizing index skips and limits parameters.

## Local Installation and Execution

1. Ensure Python 3.10+ and FastAPI/Uvicorn are installed:
   ```bash
   pip install fastapi uvicorn pydantic