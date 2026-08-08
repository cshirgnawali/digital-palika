-- ==========================================
-- Digital Palika - Tilottama Municipality
-- Table: feedback
-- ==========================================

USE digital_palika;

CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),

    message TEXT NOT NULL,

    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Verify Structure
DESCRIBE feedback;