-- ==========================================
-- Digital Palika - Tilottama Municipality
-- Table: complaint_updates
-- ==========================================

USE digital_palika;

CREATE TABLE complaint_updates (
    update_id INT AUTO_INCREMENT PRIMARY KEY,

    complaint_id INT NOT NULL,
    staff_id INT NOT NULL,

    status ENUM(
        'Pending',
        'In Progress',
        'Resolved',
        'Rejected'
    ) NOT NULL,

    remarks TEXT,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (complaint_id)
        REFERENCES complaints(complaint_id)
        ON DELETE CASCADE,

    FOREIGN KEY (staff_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Verify Structure
DESCRIBE complaint_updates;