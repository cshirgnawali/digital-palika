-- ==========================================
-- Digital Palika - Tilottama Municipality
-- Table: complaints
-- ==========================================

USE digital_palika;

CREATE TABLE complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,
    department_id INT NOT NULL,
    ward_id INT NOT NULL,

    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255),

    priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',

    status ENUM(
        'Pending',
        'In Progress',
        'Resolved',
        'Rejected'
    ) DEFAULT 'Pending',

    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
        ON DELETE CASCADE,

    FOREIGN KEY (ward_id)
        REFERENCES wards(ward_id)
        ON DELETE CASCADE
);

-- Verify Structure
DESCRIBE complaints;