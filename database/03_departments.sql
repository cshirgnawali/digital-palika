-- ==========================================
-- Digital Palika - Tilottama Municipality
-- Table: departments
-- ==========================================

USE digital_palika;

CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Initial Departments
INSERT INTO departments (department_name, description) VALUES
('Administration', 'General administration and governance'),
('Engineering', 'Roads, bridges, buildings and infrastructure'),
('Health', 'Health services and public health'),
('Education', 'Schools and educational programs'),
('Revenue', 'Tax collection and municipal revenue'),
('Sanitation', 'Waste management and sanitation'),
('Agriculture', 'Agricultural development and farmer support'),
('Water Supply', 'Water distribution and maintenance'),
('Information Technology', 'Digital services and IT support');

-- Verify Data
SELECT * FROM departments;