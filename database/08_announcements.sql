-- ==========================================
-- Digital Palika - Tilottama Municipality
-- Table: announcements
-- ==========================================

USE digital_palika;

CREATE TABLE announcements (
    announcement_id INT AUTO_INCREMENT PRIMARY KEY,

    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,

    published_by INT NOT NULL,

    publish_date DATE NOT NULL,
    expiry_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (published_by)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Verify Structure
DESCRIBE announcements;