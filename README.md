# TalentCore Systems - Employee Directory

A professional legacy employee management web application built with Python Flask and MySQL, designed as a realistic on-premises system for AWS migration demonstrations and educational purposes.

## 🚀 Features

- **Employee Management**: Add, view, and delete employee records
- **Professional Dashboard**: Real-time statistics and metrics
- **Search & Filter**: Quick employee search functionality
- **Responsive Design**: Modern, mobile-friendly interface
- **Data Validation**: Comprehensive form validation and error handling
- **Professional UI**: Clean, corporate-style design

## 📋 Employee Fields

- Employee ID (auto-generated)
- Full Name
- Email Address (unique)
- Phone Number
- Department (Engineering, Marketing, Sales, HR, Finance, Operations, Customer Support, Product)
- Job Role
- Employment Type (Full-time, Part-time, Contract, Remote, Intern)
- Hire Date
- Automatic timestamps (created_at, updated_at)

## 🛠 Technology Stack

- **Backend**: Python 3.8+ with Flask framework
- **Database**: MySQL 8.0+
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Icons**: Font Awesome 6.0
- **Styling**: Modern CSS with gradients and animations

## 📦 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd employee-management-system

# Or download and extract the ZIP file
```

### 2. Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 3. Database Setup

#### Option A: Automatic Setup (Recommended)
The application will automatically create the database and tables on first run with the correct schema including all required columns (phone, employment_type, etc.).

#### Option B: Manual Setup using SQL file
```bash
# Create the database and import schema + sample data
mysql -u root -p < database_setup.sql

# Or if using a custom user:
mysql -u your_username -p < database_setup.sql
```

#### Option C: Manual Database Creation
```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE employee_db;

# Create user (optional but recommended)
CREATE USER 'employee_app'@'localhost' IDENTIFIED BY 'employee_app_pass';
GRANT ALL PRIVILEGES ON employee_db.* TO 'employee_app'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Import schema and data
mysql -u employee_app -p employee_db < database_setup.sql
```

**Important:** The database schema includes all required columns: id, full_name, email, phone, department, role, employment_type, hire_date, created_at, updated_at.

### 4. Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your database credentials
# Default values work for standard MySQL installations
```

Example `.env` configuration:
```env
SECRET_KEY=your-secret-key-change-in-production
FLASK_DEBUG=True
DB_HOST=localhost
DB_NAME=employee_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_PORT=3306
```

### 5. Run the Application

```bash
# Start the Flask development server
python app.py
```

The application will be available at: `http://localhost:5000`

## 🖥 Usage

### Adding Employees
1. Fill out the "Add New Employee" form
2. All fields are required
3. Email addresses must be unique
4. Click "Add Employee" to save

### Viewing Employees
- All employees are displayed in the "Employee Directory" table
- Use the search box to filter employees by name, email, department, or role
- View employee count, department count, and recent hires in the dashboard

### Deleting Employees
1. Click the red trash icon next to an employee
2. Confirm deletion in the modal dialog
3. Employee will be permanently removed

## 📊 Dashboard Features

- **Total Employees**: Current employee count
- **Departments**: Number of unique departments
- **Recent Hires**: Employees hired in the last 30 days
- **Search Functionality**: Real-time employee filtering
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🔧 Configuration

### Database Configuration
Edit the `.env` file to match your MySQL setup:

```env
DB_HOST=localhost          # MySQL server host
DB_NAME=employee_db # Database name
DB_USER=root              # MySQL username
DB_PASSWORD=password      # MySQL password
DB_PORT=3306             # MySQL port
```

### Application Configuration
- `SECRET_KEY`: Change this for production deployments
- `FLASK_DEBUG`: Set to `False` for production
- `MAX_CONTENT_LENGTH`: File upload limit (currently 16MB)

## 🚀 Production Deployment

### For Linux Server Deployment:

1. **Install Dependencies**:
```bash
sudo apt update
sudo apt install python3 python3-pip mysql-server
```

2. **Setup MySQL**:
```bash
sudo mysql_secure_installation
sudo systemctl start mysql
sudo systemctl enable mysql
```

3. **Configure Application**:
```bash
# Create production .env file
cp .env.example .env
# Edit with production values
nano .env
```

4. **Run with Production Server**:
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

5. **Setup as System Service** (Optional):
Create `/etc/systemd/system/employee-management.service`:
```ini
[Unit]
Description=Employee Management System
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/venv/bin
ExecStart=/path/to/your/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📁 Project Structure

```
employee-management-system/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── database_setup.sql    # Database schema and sample data
├── .env.example         # Environment variables template
├── README.md            # This file
├── templates/
│   └── index.html       # Main HTML template
└── static/
    └── css/
        └── style.css    # Application styles
```

## 🎯 Educational Use

This project is designed for:
- **Portfolio Projects**: Demonstrate full-stack development skills
- **AWS Migration Training**: Practice migrating legacy applications to cloud
- **Web Development Learning**: Understand Flask, MySQL, and frontend integration
- **Interview Preparation**: Showcase practical development experience

## 🔒 Security Notes

- Change the `SECRET_KEY` in production
- Use environment variables for sensitive configuration
- Implement proper authentication for production use
- Consider HTTPS for production deployments
- Regular database backups recommended

## 🐛 Troubleshooting

### Common Issues:

1. **"Error adding employee" when submitting form**:
   - **Cause**: Missing database columns (phone, employment_type)
   - **Solution**: Run `mysql -u root -p employee_db < database_setup.sql` to ensure correct schema

2. **Database Connection Error**:
   - Verify MySQL is running: `sudo service mysql status`
   - Check credentials in `.env` file
   - Test connection: `mysql -u your_username -p employee_db`

3. **Table Missing Columns Error**:
   ```bash
   # Add missing columns manually if needed:
   mysql -u root -p employee_db
   ALTER TABLE employees ADD COLUMN phone VARCHAR(20) NOT NULL AFTER email;
   ALTER TABLE employees ADD COLUMN employment_type VARCHAR(20) NOT NULL AFTER role;
   ```

4. **Port Already in Use**:
   - Change port in `app.py`: `app.run(port=5001)`
   - Or kill existing process: `sudo lsof -t -i tcp:5000 | xargs kill -9`

5. **Permission Errors**:
   - Check file permissions: `chmod +x app.py`
   - Ensure MySQL user has proper privileges

6. **Module Not Found**:
   - Reinstall requirements: `pip install -r requirements.txt`
   - Check Python version: `python --version`

### Database Schema Verification:
```bash
# Check if your table has all required columns:
mysql -u root -p employee_db -e "DESCRIBE employees;"
```

Expected columns: id, full_name, email, phone, department, role, employment_type, hire_date, created_at, updated_at

## 📝 License

This project is created for educational purposes. Feel free to use, modify, and distribute for learning and portfolio development.

## 🤝 Contributing

This is an educational project. Students are encouraged to:
- Add new features (authentication, reporting, etc.)
- Improve the UI/UX design
- Optimize database queries
- Add unit tests
- Implement additional validation

## 📞 Support

For questions about this educational project:
- Review the code comments for implementation details
- Check the troubleshooting section above
- Practice debugging skills by examining error messages
- Experiment with modifications to learn more

---

**Built for TalentCore Systems - Professional Employee Management for AWS Migration Demos**