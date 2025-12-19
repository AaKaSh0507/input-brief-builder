# GPJ Input Brief Assistant

An AI-powered event input brief generation system with comprehensive features for creating, managing, and exporting event briefs.

## 🏗️ Architecture

### Tech Stack
- **Backend**: FastAPI (Python) with MVC architecture
- **Database**: PostgreSQL
- **Caching**: Redis
- **Frontend**: Vue.js 3 with Pinia state management
- **AI**: Emergent LLM (OpenAI GPT-4) via emergentintegrations

### Project Structure

```
/app/
├── backend/                    # FastAPI Backend (MVC)
│   ├── models.py              # Database models (M)
│   ├── schemas.py             # Pydantic schemas
│   ├── database.py            # Database configuration
│   ├── controllers/           # Business logic (C)
│   │   ├── brief_controller.py
│   │   ├── section_controller.py
│   │   ├── document_controller.py
│   │   └── ai_controller.py
│   ├── routes/                # API endpoints (V)
│   │   ├── brief_routes.py
│   │   ├── section_routes.py
│   │   ├── document_routes.py
│   │   └── ai_routes.py
│   ├── services/              # Utility services
│   │   ├── ai_service.py      # AI/LLM integration
│   │   ├── document_service.py # Document processing
│   │   ├── cache_service.py   # Redis caching
│   │   └── export_service.py  # PDF/Word export
│   ├── uploads/               # Uploaded documents
│   ├── exports/               # Exported briefs
│   └── server.py              # Main application
│
└── frontend/                   # Vue.js Frontend
    ├── src/
    │   ├── views/             # Page components
    │   │   ├── Dashboard.vue  # Main dashboard
    │   │   └── BriefEditor.vue # Brief creation/editing
    │   ├── components/        # Reusable components
    │   ├── stores/            # Pinia stores
    │   │   └── briefStore.js  # Brief state management
    │   ├── api/               # API client
    │   │   ├── client.js      # Axios configuration
    │   │   ├── briefs.js      # Brief API
    │   │   ├── sections.js    # Section API
    │   │   ├── documents.js   # Document API
    │   │   └── ai.js          # AI API
    │   ├── router/            # Vue Router
    │   ├── App.vue            # Root component
    │   └── index.js           # Entry point
    └── public/
```

## 🚀 Features

### Core Features
1. **Brief Management**
   - Create, read, update, delete briefs
   - Status tracking (Draft, In Progress, Completed, Archived)
   - Version control with snapshots

2. **11-Section Wizard**
   - Project Overview
   - IBM Workstream Owners
   - GPJ Planning Team
   - SVP Milestones
   - Purpose & Targets
   - Objectives & Audience
   - Integrations and Considerations
   - Content Strategy and Narrative
   - Experience Design
   - Historic Learnings
   - Additional Considerations

3. **AI-Powered Assistance**
   - Auto-populate sections from uploaded documents
   - Generate content suggestions using GPT-4
   - Extract structured data from documents
   - Field-level AI suggestions

4. **Document Management**
   - Upload documents (PDF, DOC, DOCX, CSV, PPT, PPTX, images)
   - Automatic text extraction
   - AI-powered document analysis
   - Document-to-section mapping

5. **Export & Version Control**
   - Export to PDF or Word format
   - Create version snapshots
   - Track brief history

6. **Dashboard**
   - View all briefs with status filtering
   - Statistics (Total, Draft, In Progress, Completed)
   - Search and filter capabilities

## 📝 Database Schema

### Tables

**briefs**
- id (PK)
- title
- event_type
- status (enum)
- created_at
- updated_at
- version
- brief_metadata (JSON)

**brief_sections**
- id (PK)
- brief_id (FK)
- section_number
- section_name
- content (JSON)
- ai_generated (JSON)
- created_at
- updated_at

**documents**
- id (PK)
- brief_id (FK)
- filename
- file_path
- file_type
- mime_type
- extracted_content (TEXT)
- uploaded_at

**brief_versions**
- id (PK)
- brief_id (FK)
- version_number
- content_snapshot (JSON)
- created_at

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```bash
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/gpj_briefs"
REDIS_URL="redis://localhost:6379"
CORS_ORIGINS="*"
EMERGENT_LLM_KEY=sk-emergent-6C3A9615c2e263f166
GOOGLE_SHEETS_CREDENTIALS_PATH="/app/backend/google_credentials.json"
```

**Frontend (.env)**
```bash
REACT_APP_BACKEND_URL=https://basic-spec-builder.preview.emergentagent.com
WDS_SOCKET_PORT=443
ENABLE_HEALTH_CHECK=false
```

### Google Sheets Integration

To enable Google Sheets integration, replace the placeholder in `/app/backend/google_credentials.json` with your actual Google Cloud service account credentials:

1. Go to Google Cloud Console
2. Create a service account
3. Download the JSON credentials
4. Replace the content in `google_credentials.json`

## 🔌 API Endpoints

### Brief Management
- `POST /api/briefs/` - Create a new brief
- `GET /api/briefs/` - Get all briefs (with optional status filter)
- `GET /api/briefs/{id}` - Get a specific brief
- `PUT /api/briefs/{id}` - Update a brief
- `DELETE /api/briefs/{id}` - Delete a brief
- `GET /api/briefs/{id}/export?format=pdf` - Export brief to PDF/Word
- `POST /api/briefs/{id}/versions` - Create a version snapshot
- `GET /api/briefs/{id}/versions` - Get all versions

### Section Management
- `GET /api/sections/brief/{brief_id}` - Get all sections for a brief
- `GET /api/sections/{id}` - Get a specific section
- `PUT /api/sections/{id}` - Update a section
- `POST /api/sections/` - Create a custom section
- `DELETE /api/sections/{id}` - Delete a section

### Document Management
- `POST /api/documents/upload?brief_id={id}` - Upload a document
- `GET /api/documents/brief/{brief_id}` - Get all documents for a brief
- `GET /api/documents/{id}` - Get a specific document
- `POST /api/documents/{id}/analyze?section_name={name}` - Analyze document with AI
- `DELETE /api/documents/{id}` - Delete a document

### AI Features
- `POST /api/ai/generate/{section_id}` - Generate AI content for a section
- `POST /api/ai/suggestions?field_name={name}` - Get AI suggestions for a field
- `POST /api/ai/auto-populate/{section_id}?brief_id={id}` - Auto-populate from documents

## 🎯 Usage Guide

### Creating a New Brief

1. Navigate to the dashboard
2. Click "New Brief" button
3. Enter brief title and event type
4. System automatically creates all 11 sections
5. Fill in sections using the wizard interface

### Using AI Features

**Auto-populate from Documents:**
1. Upload documents to your brief
2. Navigate to any section
3. Click "Auto-populate from docs"
4. AI extracts relevant information from all uploaded documents

**Generate AI Content:**
1. Fill in some context in the section
2. Click "Generate AI" button
3. AI generates suggestions based on context
4. Review and incorporate suggestions

**Upload Documents:**
- Supported formats: PDF, DOC, DOCX, CSV, PPT, PPTX, PNG, JPG
- Documents are automatically processed
- Text is extracted for AI analysis

### Exporting Briefs

1. Complete all required sections
2. Click "Export PDF" or "Export Word"
3. File downloads automatically
4. Includes all sections with proper formatting

## 🔒 Security & Performance

### Caching
- Redis caching for brief data
- 1-hour TTL for cached items
- Automatic cache invalidation on updates

### Security
- CORS configuration
- Input validation using Pydantic
- SQL injection protection via SQLAlchemy ORM
- File upload size limits

### Performance
- Lazy loading of sections
- Pagination support for brief lists
- Async operations for AI calls
- Connection pooling for database

## 🚀 Running the Application

### Services
All services are managed by Supervisor:

```bash
# Check status
sudo supervisorctl status

# Restart services
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
sudo supervisorctl restart all
```

### Services Running:
- **Backend**: http://localhost:8001
- **Frontend**: http://localhost:3000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Health Check
```bash
curl http://localhost:8001/api/health
```

## 📊 System Requirements

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+
- 2GB RAM minimum
- 10GB disk space

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop (optimized for 1920x1080)
- **Minimal UI**: Clean, professional interface
- **Real-time Updates**: Instant feedback on actions
- **Status Indicators**: Visual status badges for briefs
- **Navigation**: Section-by-section wizard with progress tracking
- **Keyboard Shortcuts**: Quick navigation between sections

## 🤖 AI Models Used

- **Text Generation**: OpenAI GPT-4o via Emergent LLM Key
- **Document Analysis**: Gemini 2.5 Flash (supports file attachments)
- **Universal Key**: Single key works across OpenAI, Anthropic, and Google

## 📝 Notes

1. **Single User System**: Designed for individual use, no complex authentication
2. **No Approval Workflows**: Removed as per requirements
3. **Google Sheets**: Placeholder credentials provided - add your own
4. **Emergent LLM Key**: Pre-configured, deducts from your balance
5. **Auto-save**: Sections are saved when navigating between them

## 🐛 Troubleshooting

### Backend not starting?
```bash
tail -50 /var/log/supervisor/backend.err.log
```

### Frontend not loading?
```bash
tail -50 /var/log/supervisor/frontend.err.log
```

### Database connection issues?
```bash
sudo -u postgres psql -c "SELECT 1"
```

### Redis not working?
```bash
redis-cli ping
```

## 📞 Support

For issues or questions:
1. Check logs in `/var/log/supervisor/`
2. Verify all services are running
3. Check database connectivity
4. Ensure ports 3000 and 8001 are accessible

---

**Built with ❤️ using Emergent Platform**
