-- ==========================================
-- Digital Palika - Tilottama Municipality
-- Table: budgets
-- ==========================================

USE digital_palika;

CREATE TABLE budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,

    project_id INT NOT NULL,

    fiscal_year VARCHAR(20) NOT NULL,

    allocated_amount DECIMAL(15,2) NOT NULL,
    spent_amount DECIMAL(15,2) DEFAULT 0.00,

    budget_status ENUM(
        'Allocated',
        'In Progress',
        'Completed'
    ) DEFAULT 'Allocated',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
);

-- Verify Structure
DESCRIBE budgets;