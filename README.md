# Agreemate - Legal Document Automation Platform

A comprehensive fullstack application for automating legal document creation with eStamp and eSign integration using Leegality APIs.

## 🏗️ Architecture

- **Backend**: FastAPI (Python) with JWT authentication
- **Frontend**: React + TypeScript with Tailwind CSS
- **Database**: In-memory (PostgreSQL-ready)
- **APIs**: Leegality integration for eStamp/eSign
- **Deployment**: Ready for production deployment

## 📁 Project Structure

```
agreemate-fullstack/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── core/           # Configuration and security
│   │   ├── models/         # Data models
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # Business logic
│   │   └── templates/      # Agreement templates
│   ├── pyproject.toml      # Python dependencies
│   └── .env               # Environment variables
└── frontend/               # React frontend application
    ├── src/
    │   ├── components/     # UI components
    │   ├── contexts/       # React contexts
    │   ├── pages/         # Application pages
    │   └── lib/           # Utilities
    ├── package.json       # Node dependencies
    └── .env              # Frontend environment variables
```

## 🚀 Features

### Core Functionality
- **Agreement Template Engine**: Dynamic templates with placeholder replacement
- **PDF Generation**: Professional document generation with ReportLab
- **User Authentication**: JWT-based auth with registration/login
- **Document Tracking**: Complete status tracking from draft to completion

### Leegality Integration
- **eStamp Service**: Real/mock stamp paper integration
- **eSign Service**: Aadhaar-based digital signatures
- **Status Monitoring**: Real-time signature tracking
- **Webhook Support**: Callback handling for status updates

### Frontend Features
- **Modern UI**: Tailwind CSS with shadcn/ui components
- **Responsive Design**: Mobile-first approach
- **Real-time Updates**: Dynamic status tracking
- **Form Validation**: Comprehensive input validation

## 🛠️ Setup & Installation

### Backend Setup

```bash
cd backend
poetry install
cp .env.example .env  # Configure your environment variables
poetry run fastapi dev app/main.py --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env  # Configure your environment variables
npm run dev
```

## 🔧 Configuration

### Backend Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/agreemate

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Leegality API
LEEGALITY_AUTH_TOKEN=your_leegality_auth_token_here
LEEGALITY_BASE_URL=https://sandbox.leegality.com/api/v2.1
LEEGALITY_ENABLED=false  # Set to true for production

# File Storage
UPLOAD_DIR=./uploads
```

### Frontend Environment Variables

```env
VITE_API_URL=http://localhost:8000
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `POST /agreements/` - Create new agreement
- `POST /agreements/{id}/estamp` - Request eStamp
- `POST /agreements/{id}/esign` - Initiate eSign
- `GET /agreements/{id}` - Get agreement details

## 🧪 Testing

### Backend Testing

```bash
cd backend
poetry run pytest
```

### Frontend Testing

```bash
cd frontend
npm run test
```

### Manual Testing

1. Start both backend and frontend servers
2. Register a new user account
3. Create a test agreement
4. Test eStamp functionality
5. Test eSign workflow
6. Verify status updates

## 🚀 Deployment

### Backend Deployment

The backend is ready for deployment on platforms like:
- Railway
- Render
- AWS EC2
- Google Cloud Run

### Frontend Deployment

The frontend can be deployed on:
- Vercel
- Netlify
- AWS S3 + CloudFront

## 🔐 Security Features

- JWT token authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation and sanitization
- File upload security

## 📋 Agreement Types Supported

1. **Rental Agreements**
   - Landlord/tenant details
   - Property information
   - Rent and deposit amounts

2. **Employment Contracts**
   - Employer/employee details
   - Job role and responsibilities
   - Salary and benefits

3. **Service Agreements**
   - Service provider/client details
   - Scope of work
   - Payment terms

## 🔄 Workflow

1. **User Registration/Login**
2. **Agreement Creation** - Select type and fill details
3. **eStamp Processing** - Automatic stamp duty calculation and payment
4. **eSign Initiation** - Send signing links to all parties
5. **Document Completion** - Final signed document generation
6. **Download & Share** - Access completed legal documents

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Email: support@agreemate.com
- Documentation: [API Docs](http://localhost:8000/docs)
- Issues: GitHub Issues

---

Built with ❤️ for simplifying legal document automation in India.
