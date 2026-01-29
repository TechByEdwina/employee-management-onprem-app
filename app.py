from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import logging

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'employee_db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None

def init_database():
    """Initialize the database and create tables if they don't exist"""
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            cursor.execute(f"USE {DB_CONFIG['database']}")
            
            # Create employees table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20) NOT NULL,
                department VARCHAR(50) NOT NULL,
                role VARCHAR(50) NOT NULL,
                employment_type VARCHAR(20) NOT NULL,
                hire_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                
                -- Indexes for better performance
                INDEX idx_department (department),
                INDEX idx_employment_type (employment_type),
                INDEX idx_hire_date (hire_date),
                INDEX idx_email (email)
            )
            """
            cursor.execute(create_table_query)
            
            # Check if phone column exists and add it if missing (migration)
            cursor.execute("SHOW COLUMNS FROM employees LIKE 'phone'")
            phone_column_exists = cursor.fetchone()
            
            if not phone_column_exists:
                logger.info("Phone column missing, adding it...")
                cursor.execute("ALTER TABLE employees ADD COLUMN phone VARCHAR(20) NOT NULL DEFAULT ''")
                logger.info("Phone column added successfully")
            
            connection.commit()
            logger.info("Database initialized successfully")
            
    except Error as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/')
def index():
    """Main page displaying all employees and add form"""
    employees = get_all_employees()
    stats = get_employee_stats()
    return render_template('index.html', employees=employees, stats=stats)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    """Add a new employee to the database"""
    try:
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        department = request.form.get('department', '').strip()
        role = request.form.get('role', '').strip()
        employment_type = request.form.get('employment_type', '').strip()
        hire_date = request.form.get('hire_date', '').strip()
        
        # Validation
        if not all([full_name, email, phone, department, role, employment_type, hire_date]):
            flash('All fields are required!', 'error')
            return redirect(url_for('index'))
        
        # Validate email format
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address!', 'error')
            return redirect(url_for('index'))
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            insert_query = """
            INSERT INTO employees (full_name, email, phone, department, role, employment_type, hire_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (full_name, email, phone, department, role, employment_type, hire_date))
            connection.commit()
            
            flash(f'Employee {full_name} added successfully!', 'success')
            logger.info(f"Added new employee: {full_name}")
            
    except mysql.connector.IntegrityError:
        flash('Email address already exists!', 'error')
    except Error as e:
        flash('Error adding employee. Please try again.', 'error')
        logger.error(f"Error adding employee: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    
    return redirect(url_for('index'))

@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    """Delete an employee from the database"""
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            # Get employee name for confirmation message
            cursor.execute("SELECT full_name FROM employees WHERE id = %s", (employee_id,))
            result = cursor.fetchone()
            
            if result:
                employee_name = result[0]
                cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
                connection.commit()
                flash(f'Employee {employee_name} deleted successfully!', 'success')
                logger.info(f"Deleted employee: {employee_name}")
            else:
                flash('Employee not found!', 'error')
                
    except Error as e:
        flash('Error deleting employee. Please try again.', 'error')
        logger.error(f"Error deleting employee: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    
    return redirect(url_for('index'))

def get_all_employees():
    """Retrieve all employees from the database"""
    employees = []
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, full_name, email, phone, department, role, employment_type, hire_date 
                FROM employees 
                ORDER BY created_at DESC
            """)
            employees = cursor.fetchall()
            
    except Error as e:
        logger.error(f"Error retrieving employees: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    
    return employees

def get_employee_stats():
    """Get employee statistics for dashboard"""
    stats = {
        'total_employees': 0,
        'departments': 0,
        'recent_hires': 0
    }
    
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            # Total employees
            cursor.execute("SELECT COUNT(*) FROM employees")
            stats['total_employees'] = cursor.fetchone()[0]
            
            # Unique departments
            cursor.execute("SELECT COUNT(DISTINCT department) FROM employees")
            stats['departments'] = cursor.fetchone()[0]
            
            # Recent hires (last 30 days)
            cursor.execute("""
                SELECT COUNT(*) FROM employees 
                WHERE hire_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            """)
            stats['recent_hires'] = cursor.fetchone()[0]
            
    except Error as e:
        logger.error(f"Error getting stats: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    
    return stats

@app.route('/api/employees')
def api_employees():
    """API endpoint to get all employees as JSON"""
    employees = get_all_employees()
    # Convert date objects to strings for JSON serialization
    for employee in employees:
        if employee['hire_date']:
            employee['hire_date'] = employee['hire_date'].strftime('%Y-%m-%d')
    return jsonify(employees)

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)