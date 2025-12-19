# GPJ Input Brief Assistant - API Documentation

## Base URL
```
http://localhost:8001/api
```

---

## 📋 Brief Management

### Create Brief
**POST** `/briefs/`

Creates a new brief and automatically initializes all 11 sections.

**Request Body:**
```json
{
  "title": "IBM Think Conference 2025",
  "event_type": "Conference",
  "brief_metadata": {
    "client": "IBM",
    "location": "Las Vegas"
  }
}
```

**Response:**
```json
{
  "id": "uuid",
  "title": "IBM Think Conference 2025",
  "event_type": "Conference",
  "status": "draft",
  "created_at": "2025-12-19T08:57:44.160066",
  "updated_at": "2025-12-19T08:57:44.160068",
  "version": 1,
  "brief_metadata": {
    "client": "IBM",
    "location": "Las Vegas"
  }
}
```

### Get All Briefs
**GET** `/briefs/?status={status}&skip={skip}&limit={limit}`

**Query Parameters:**
- `status` (optional): Filter by status (draft, in_progress, completed, archived)
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 100)

**Example:**
```bash
curl http://localhost:8001/api/briefs/?status=in_progress&limit=10
```

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "Event Title",
    "event_type": "Conference",
    "status": "in_progress",
    "created_at": "2025-12-19T08:57:44.160066",
    "updated_at": "2025-12-19T08:57:44.160068",
    "version": 1,
    "brief_metadata": {}
  }
]
```

### Get Single Brief
**GET** `/briefs/{brief_id}`

**Response:**
```json
{
  "id": "uuid",
  "title": "Event Title",
  "event_type": "Conference",
  "status": "draft",
  "created_at": "2025-12-19T08:57:44.160066",
  "updated_at": "2025-12-19T08:57:44.160068",
  "version": 1,
  "brief_metadata": {}
}
```

### Update Brief
**PUT** `/briefs/{brief_id}`

**Request Body:**
```json
{
  "title": "Updated Title",
  "status": "in_progress"
}
```

### Delete Brief
**DELETE** `/briefs/{brief_id}`

**Response:** 204 No Content

### Export Brief
**GET** `/briefs/{brief_id}/export?format={format}`

**Query Parameters:**
- `format`: pdf or word

**Response:** File download (application/octet-stream)

**Example:**
```bash
curl -O http://localhost:8001/api/briefs/{id}/export?format=pdf
```

### Create Version Snapshot
**POST** `/briefs/{brief_id}/versions`

Creates a snapshot of the current brief state.

**Response:**
```json
{
  "version_number": 2,
  "created_at": "2025-12-19T09:00:00"
}
```

### Get All Versions
**GET** `/briefs/{brief_id}/versions`

**Response:**
```json
[
  {
    "id": "uuid",
    "version_number": 2,
    "created_at": "2025-12-19T09:00:00"
  },
  {
    "id": "uuid",
    "version_number": 1,
    "created_at": "2025-12-19T08:57:44"
  }
]
```

---

## 📄 Section Management

### Get Brief Sections
**GET** `/sections/brief/{brief_id}`

Returns all 11 sections for a brief in order.

**Response:**
```json
[
  {
    "id": "uuid",
    "brief_id": "brief-uuid",
    "section_number": 1,
    "section_name": "Project Overview",
    "content": {
      "description": "Event description",
      "goals": "Event goals"
    },
    "ai_generated": {
      "generated_text": "AI suggested content"
    },
    "created_at": "2025-12-19T08:57:44",
    "updated_at": "2025-12-19T08:57:44"
  }
]
```

### Get Single Section
**GET** `/sections/{section_id}`

### Update Section
**PUT** `/sections/{section_id}`

**Request Body:**
```json
{
  "content": {
    "description": "Updated description",
    "goals": "Updated goals",
    "custom_field": "Custom value"
  }
}
```

**Response:**
```json
{
  "id": "uuid",
  "brief_id": "brief-uuid",
  "section_number": 1,
  "section_name": "Project Overview",
  "content": {
    "description": "Updated description",
    "goals": "Updated goals",
    "custom_field": "Custom value"
  },
  "ai_generated": {},
  "created_at": "2025-12-19T08:57:44",
  "updated_at": "2025-12-19T09:05:30"
}
```

### Create Custom Section
**POST** `/sections/?brief_id={brief_id}`

**Request Body:**
```json
{
  "section_number": 12,
  "section_name": "Custom Section",
  "content": {}
}
```

### Delete Section
**DELETE** `/sections/{section_id}`

---

## 📎 Document Management

### Upload Document
**POST** `/documents/upload?brief_id={brief_id}`

**Content-Type:** multipart/form-data

**Form Data:**
- `file`: The document file

**Supported Formats:**
- PDF (.pdf)
- Word (.doc, .docx)
- CSV (.csv)
- PowerPoint (.ppt, .pptx)
- Images (.png, .jpg, .jpeg)

**Example (curl):**
```bash
curl -X POST "http://localhost:8001/api/documents/upload?brief_id={brief_id}" \
  -F "file=@/path/to/document.pdf"
```

**Response:**
```json
{
  "id": "uuid",
  "brief_id": "brief-uuid",
  "filename": "document.pdf",
  "file_type": "pdf",
  "uploaded_at": "2025-12-19T09:10:00",
  "extracted_content": "Extracted text content from document..."
}
```

### Get Brief Documents
**GET** `/documents/brief/{brief_id}`

**Response:**
```json
[
  {
    "id": "uuid",
    "brief_id": "brief-uuid",
    "filename": "document.pdf",
    "file_type": "pdf",
    "uploaded_at": "2025-12-19T09:10:00",
    "extracted_content": "Extracted text..."
  }
]
```

### Get Single Document
**GET** `/documents/{document_id}`

### Analyze Document with AI
**POST** `/documents/{document_id}/analyze?section_name={section_name}`

Analyzes a document with AI to extract information for a specific section.

**Example:**
```bash
curl -X POST "http://localhost:8001/api/documents/{doc_id}/analyze?section_name=Project%20Overview"
```

**Response:**
```json
{
  "document_id": "uuid",
  "analysis": {
    "event_name": "IBM Think Conference",
    "date": "March 2025",
    "location": "Las Vegas",
    "objectives": ["Objective 1", "Objective 2"]
  }
}
```

### Delete Document
**DELETE** `/documents/{document_id}`

---

## 🤖 AI Features

### Generate Section Content
**POST** `/ai/generate/{section_id}`

Generates AI content for a section based on context.

**Request Body:**
```json
{
  "section_name": "Project Overview",
  "context": {
    "event_type": "Conference",
    "client": "IBM",
    "existing_info": "Some context"
  },
  "prompt": "Optional custom prompt for AI"
}
```

**Response:**
```json
{
  "generated_text": "AI generated content based on context...",
  "section_name": "Project Overview"
}
```

### Get Field Suggestions
**POST** `/ai/suggestions?field_name={field_name}`

Get AI suggestions for a specific field.

**Request Body:**
```json
{
  "event_type": "Conference",
  "context": "Additional context"
}
```

**Response:**
```json
{
  "field_name": "objectives",
  "suggestions": [
    "Increase brand awareness",
    "Generate leads",
    "Engage with customers",
    "Launch new products",
    "Build partnerships"
  ]
}
```

### Auto-Populate Section from Documents
**POST** `/ai/auto-populate/{section_id}?brief_id={brief_id}`

Automatically populates a section by analyzing all uploaded documents for the brief.

**Response:**
```json
{
  "event_name": "IBM Think Conference",
  "objectives": "Extracted objectives from documents",
  "target_audience": "Extracted audience info",
  "key_messages": "Extracted key messages"
}
```

---

## 🔍 Common Use Cases

### Use Case 1: Creating a Complete Brief

```bash
# 1. Create brief
curl -X POST http://localhost:8001/api/briefs/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Event", "event_type": "Conference", "brief_metadata": {}}'

# Response includes brief_id

# 2. Upload documents
curl -X POST "http://localhost:8001/api/documents/upload?brief_id={brief_id}" \
  -F "file=@event_brief.pdf"

# 3. Get sections
curl http://localhost:8001/api/sections/brief/{brief_id}

# 4. Auto-populate first section
curl -X POST "http://localhost:8001/api/ai/auto-populate/{section_id}?brief_id={brief_id}"

# 5. Update section with manual edits
curl -X PUT http://localhost:8001/api/sections/{section_id} \
  -H "Content-Type: application/json" \
  -d '{"content": {"description": "Updated", "goals": "Goals"}}'

# 6. Export final brief
curl -O "http://localhost:8001/api/briefs/{brief_id}/export?format=pdf"
```

### Use Case 2: AI-Assisted Section Completion

```bash
# 1. Get section
curl http://localhost:8001/api/sections/{section_id}

# 2. Generate AI content
curl -X POST http://localhost:8001/api/ai/generate/{section_id} \
  -H "Content-Type: application/json" \
  -d '{
    "section_name": "Objectives & Audience",
    "context": {"event_type": "Conference", "client": "IBM"},
    "prompt": "Generate objectives and target audience"
  }'

# 3. Get field suggestions
curl -X POST "http://localhost:8001/api/ai/suggestions?field_name=target_audience" \
  -H "Content-Type: application/json" \
  -d '{"event_type": "Conference"}'

# 4. Update section with final content
curl -X PUT http://localhost:8001/api/sections/{section_id} \
  -H "Content-Type: application/json" \
  -d '{"content": {"objectives": "Final objectives", "audience": "Final audience"}}'
```

---

## 📊 Status Codes

- `200 OK` - Successful GET/PUT request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid input data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## 🔐 Error Responses

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

**Example Errors:**

```json
{
  "detail": "Brief not found"
}
```

```json
{
  "detail": "Section not found"
}
```

```json
{
  "detail": "Failed to upload document"
}
```

---

## 💡 Tips

1. **Always create brief first** - Sections are auto-created
2. **Upload documents early** - Enables AI auto-population
3. **Use AI features** - Saves time on content creation
4. **Create versions** - Before major changes
5. **Export regularly** - Keep backups of your work

---

**For more information, see README.md**
