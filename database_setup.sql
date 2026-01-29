-- Employee Management System Database Setup
-- This script creates the database and tables for the employee management system

-- Create database
CREATE DATABASE IF NOT EXISTS employee_db;
USE employee_db;

-- Create employees table
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
);

-- Insert sample data for demonstration
INSERT INTO employees (full_name, email, phone, department, role, employment_type, hire_date) VALUES
('Sarah Johnson', 'sarah.johnson@talentcore.com', '(555) 123-4567', 'Engineering', 'Senior Software Engineer', 'Full-time', '2023-01-15'),
('Michael Chen', 'michael.chen@talentcore.com', '(555) 234-5678', 'Engineering', 'DevOps Engineer', 'Remote', '2023-02-20'),
('Emily Rodriguez', 'emily.rodriguez@talentcore.com', '(555) 345-6789', 'Marketing', 'Marketing Manager', 'Full-time', '2023-03-10'),
('David Kim', 'david.kim@talentcore.com', '(555) 456-7890', 'Sales', 'Sales Representative', 'Full-time', '2023-04-05'),
('Lisa Thompson', 'lisa.thompson@talentcore.com', '(555) 567-8901', 'Human Resources', 'HR Specialist', 'Part-time', '2023-05-12'),
('James Wilson', 'james.wilson@talentcore.com', '(555) 678-9012', 'Finance', 'Financial Analyst', 'Contract', '2023-06-18'),
('Maria Garcia', 'maria.garcia@talentcore.com', '(555) 789-0123', 'Customer Support', 'Support Specialist', 'Full-time', '2023-07-22'),
('Robert Brown', 'robert.brown@talentcore.com', '(555) 890-1234', 'Operations', 'Operations Manager', 'Full-time', '2023-08-30');

-- Create a view for employee statistics
CREATE OR REPLACE VIEW employee_stats AS
SELECT 
    COUNT(*) as total_employees,
    COUNT(DISTINCT department) as total_departments,
    COUNT(CASE WHEN hire_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN 1 END) as recent_hires_30_days,
    COUNT(CASE WHEN hire_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY) THEN 1 END) as recent_hires_90_days
FROM employees;

-- Create a view for department summary
CREATE OR REPLACE VIEW department_summary AS
SELECT 
    department,
    COUNT(*) as employee_count,
    MIN(hire_date) as earliest_hire,
    MAX(hire_date) as latest_hire
FROM employees
GROUP BY department
ORDER BY employee_count DESC;