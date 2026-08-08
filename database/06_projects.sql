-- ==========================================
-- Digital Palika - Tilottama Municipality
-- Table: projects
-- ==========================================

USE digital_palika;

CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,

    department_id INT NOT NULL,
    ward_id INT NOT NULL,

    project_name VARCHAR(200) NOT NULL,
    description TEXT,

    estimated_cost DECIMAL(15,2) NOT NULL,

    start_date DATE,
    expected_end_date DATE,

    status ENUM(
        'Planned',
        'Ongoing',
        'Completed',
        'Cancelled'
    ) DEFAULT 'Planned',

    contractor_name VARCHAR(150),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
        ON DELETE CASCADE,

    FOREIGN KEY (ward_id)
        REFERENCES wards(ward_id)
        ON DELETE CASCADE
);

-- Verify Structure
DESCRIBE projects;