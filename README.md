# 🏢 Customer 360 - Professional Customer Management System

A modern, full-featured customer relationship management (CRM) system built with Django. Customer 360 provides comprehensive customer management, interaction tracking, and analytics in a beautiful, responsive interface.

![Customer 360 Dashboard](https://img.shields.io/badge/Django-4.2.23-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=for-the-badge&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## ✨ Features

### 👥 Customer Management
- **Complete Customer Profiles** - Store comprehensive customer information
- **Advanced Search & Filtering** - Find customers quickly with powerful search
- **Active/Inactive Status** - Soft delete functionality preserves data
- **Bulk Operations** - Manage multiple customers efficiently
- **Data Validation** - Robust form validation and error handling

### 💬 Interaction Tracking
- **Multi-Channel Support** - Phone, Email, SMS, Social Media, In-Person, Chat
- **Direction Tracking** - Inbound vs Outbound communication
- **Status Management** - Pending, Completed, Follow-up Required
- **Rich Notes** - Detailed interaction summaries and notes
- **User Attribution** - Track who recorded each interaction

### 📊 Analytics Dashboard
- **Real-time Metrics** - Total interactions, recent activity, trends
- **Channel Breakdown** - Analyze communication preferences
- **Status Distribution** - Monitor interaction completion rates
- **Top Customers** - Identify most active customers
- **Time-based Analysis** - 7-day and 30-day activity views

### 🎨 Modern UI/UX
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Dark Mode Support** - Automatic dark/light theme detection
- **Smooth Animations** - Polished interactions and transitions
- **Professional Styling** - Modern gradients, shadows, and typography
- **Accessibility** - WCAG compliant with keyboard navigation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/customer360.git
   cd customer360
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your settings (optional for development)
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser to `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`


### Dashboard Overview
Beautiful, modern dashboard with real-time metrics and analytics.

### Customer Management
Comprehensive customer profiles with search, filtering, and bulk operations.

### Interaction Tracking
Multi-channel interaction logging with rich notes and status tracking.

### Analytics & Reporting
Detailed analytics with charts, trends, and customer insights.

## 🛠️ Technology Stack

### Backend
- **Django 4.2.23** - Web framework
- **SQLite** - Database (configurable to PostgreSQL/MySQL)
- **Django REST Framework** - API endpoints
- **Python Decouple** - Environment management

### Frontend
- **Bootstrap 5.3** - CSS framework
- **Bootstrap Icons** - Icon library
- **Inter Font** - Modern typography
- **Custom CSS** - Enhanced styling with gradients and animations
- **Vanilla JavaScript** - Interactive enhancements

### Development Tools
- **Django Debug Toolbar** - Development debugging
- **Django Extensions** - Additional management commands
- **Git** - Version control

## 📁 Project Structure

```
customer360/
├── customer360/           # Main project directory
│   ├── settings.py       # Django settings
│   ├── urls.py          # URL routing
│   ├── static/          # Static files (CSS, JS, images)
│   └── templates/       # Global templates
├── customer_management/   # Customer management app
│   ├── models.py        # Customer data models
│   ├── views.py         # Customer views and logic
│   ├── forms.py         # Customer forms
│   ├── urls.py          # Customer URL patterns
│   └── templates/       # Customer templates
├── interactions/         # Interaction tracking app
│   ├── models.py        # Interaction data models
│   ├── views.py         # Interaction views and logic
│   ├── forms.py         # Interaction forms
│   ├── urls.py          # Interaction URL patterns
│   └── templates/       # Interaction templates
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=sqlite:///db.sqlite3

# Security (for production)
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# Logging
LOG_LEVEL=INFO
```

### Database Options
The application supports multiple databases:

**SQLite (Default)**
```env
DATABASE_URL=sqlite:///db.sqlite3
```

**PostgreSQL**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/customer360
```

**MySQL**
```env
DATABASE_URL=mysql://user:password@localhost:3306/customer360
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in environment
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up production database
- [ ] Configure static file serving
- [ ] Set up HTTPS
- [ ] Configure logging
- [ ] Set strong `SECRET_KEY`

### Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests** (if applicable)
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Write descriptive commit messages
- Add docstrings to functions and classes
- Test your changes thoroughly
- Update documentation as needed

## 📝 API Documentation

### Customer Endpoints
- `GET /api/customers/` - List customers
- `POST /api/customers/` - Create customer
- `GET /api/customers/{id}/` - Get customer details
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer

### Interaction Endpoints
- `GET /api/interactions/` - List interactions
- `POST /api/interactions/` - Create interaction
- `GET /api/interactions/{id}/` - Get interaction details
- `PUT /api/interactions/{id}/` - Update interaction
- `DELETE /api/interactions/{id}/` - Delete interaction

## 🔒 Security Features

- **CSRF Protection** - Built-in Django CSRF protection
- **SQL Injection Prevention** - Django ORM prevents SQL injection
- **XSS Protection** - Template auto-escaping
- **Secure Headers** - Security middleware enabled
- **Input Validation** - Comprehensive form validation
- **Soft Deletes** - Data preservation with soft delete

## 📊 Performance

- **Database Optimization** - Efficient queries with select_related
- **Static File Optimization** - Compressed CSS and JS
- **Caching Ready** - Redis/Memcached support
- **Pagination** - Large datasets handled efficiently
- **Lazy Loading** - Images and content loaded on demand

## 🐛 Troubleshooting

### Common Issues

**Migration Errors**
```bash
python manage.py migrate --fake-initial
```

**Static Files Not Loading**
```bash
python manage.py collectstatic --clear
```

**Permission Errors**
```bash
# Check file permissions
chmod +x manage.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Team** - For the amazing web framework
- **Bootstrap Team** - For the responsive CSS framework
- **Bootstrap Icons** - For the comprehensive icon library
- **Inter Font** - For the beautiful typography
- **Open Source Community** - For inspiration and tools

## 📞 Support

If you encounter any issues or have questions:

1. **Check the documentation** above
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Join the discussion** in GitHub Discussions

---

**Made with ❤️ using Django and Bootstrap**

*Customer 360 - Empowering businesses with comprehensive customer relationship management.*