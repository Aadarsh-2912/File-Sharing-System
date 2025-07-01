# File Sharing System API

## Overview
A FastAPI-based file sharing system with user authentication, email verification, and file upload/download features. Supports two user roles: `ops` (operations) and `client`.

---

## Requirements
- Python 3.8+
- pip

## Installation
1. Clone the repository and navigate to the project directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables
Create a `.env` file in the root directory with the following variables:

```
# Database (default is SQLite)
DATABASE_URL=sqlite:///./test.db

# JWT Secret
SECRET_KEY=your-secret-key

# S3 Storage
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_S3_BUCKET_NAME=your-bucket-name
AWS_S3_REGION=your-region

# (Optional) Base URL for email verification links
BASE_URL=https://file-sharing-system-gvyz.onrender.com
```

---

## Running the Server
Start the FastAPI server with:
```bash
uvicorn app.main:app --reload
```
The API will be available at [https://file-sharing-system-gvyz.onrender.com](https://file-sharing-system-gvyz.onrender.com)

---

## API Endpoints

### 1. **Root**
- **GET /**
  - Returns: `{ "message": "File Sharing System API is running" }`

### 2. **Authentication** (`/auth`)

#### a. **Sign Up**
- **POST /auth/signup**
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword",
    "role": "ops" | "client"
  }
  ```
- **Response:** User info (see schemas)
- **Notes:**
  - If `role` is `client`, a verification email is simulated (see console output).

#### b. **Login**
- **POST /auth/login**
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Response:** `{ "access_token": "...", "token_type": "bearer" }`
- **Notes:**
  - Clients must verify their email before logging in.

#### c. **Verify Email**
- **GET /auth/verify-email?token=...**
- **Query Param:** `token` (from the verification email/console)
- **Response:** `{ "message": "Email verified successfully" }`

---

### 3. **File Operations** (`/files`)

#### a. **Upload File**
- **POST /files/upload**
- **Headers:**
  - `Authorization: Bearer <access_token>` (must be an `ops` user)
- **Body (form-data):**
  - `uploaded_file`: (file, required; only .pptx, .docx, .xlsx allowed)
- **Response:** `{ "message": "File uploaded successfully", "file_id": <id> }`

#### b. **Download File**
- **GET /files/download/{file_id}**
- **Headers:**
  - `Authorization: Bearer <access_token>` (must be a `client` user)
- **Response:** `{ "download-link": "<presigned_url>", "message": "success" }`

#### c. **List Files**
- **GET /files/list**
- **Headers:**
  - `Authorization: Bearer <access_token>` (must be a `client` user)
- **Response:**
  ```json
  [
    {
      "id": 1,
      "filename": "example.docx",
      "file_type": "docx",
      "uploaded_by": 2,
      "upload_time": "2024-06-01T12:00:00"
    },
    ...
  ]
  ```

---

## Testing with Postman

1. **Start the server** (`uvicorn app.main:app --reload`).
2. **Import Endpoints:**
   - Use the above endpoint details to create requests in Postman.
   - Set the base URL to `https://file-sharing-system-gvyz.onrender.com`.

3. **Workflow Example:**
   1. **Sign Up** two users: one with `role: ops`, one with `role: client`.
   2. **Verify** the client user:
      - Copy the verification link from the server console output.
      - Paste it in your browser or use a GET request in Postman.
   3. **Login** both users to get their `access_token`.
   4. **Upload a file** as the `ops` user (POST `/files/upload`, add file in form-data, set Authorization header).
   5. **List files** as the `client` user (GET `/files/list`, set Authorization header).
   6. **Download a file** as the `client` user (GET `/files/download/{file_id}`, set Authorization header).

4. **Authorization:**
   - For protected endpoints, add a header:
     - `Authorization: Bearer <access_token>`

---

## Notes
- **Roles:**
  - `ops` users can upload files.
  - `client` users can list and download files (after email verification).
- **Email:**
  - Email sending is simulated; check your server console for verification links.
- **S3:**
  - Ensure your AWS credentials and bucket are set up for file upload/download.
- **Database:**
  - Default is SQLite (`test.db`). For production, set `DATABASE_URL` to your PostgreSQL URI.

---

## FastAPI Docs
Interactive API docs are available at [https://file-sharing-system-gvyz.onrender.com/docs](https://file-sharing-system-gvyz.onrender.com/docs)

---

## License
MIT 