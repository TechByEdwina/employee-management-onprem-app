-- Fix for missing 'phone' column in employees table
-- Run this SQL script to add the missing column to your existing database

USE employee_db;

-- Add the missing phone column
ALTER TABLE employees 
ADD COLUMN phone VARCHAR(20) NOT NULL DEFAULT '';

-- Update the column to allow NULL temporarily if you have existing data
ALTER TABLE employees 
MODIFY COLUMN phone VARCHAR(20) NULL;

-- If you want to add some sample phone numbers to existing records (optional)
-- UPDATE employees SET phone = '(555) 000-0000' WHERE phone IS NULL OR phone = '';

-- Show the updated table structure
DESCRIBE employees;