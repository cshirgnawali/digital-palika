-- ==========================================
-- Digital Palika - Tilottama Municipality
-- Table: wards
-- ==========================================

USE digital_palika;

CREATE TABLE wards (
    ward_id INT AUTO_INCREMENT PRIMARY KEY,
    ward_number INT NOT NULL UNIQUE,
    ward_name VARCHAR(100) NOT NULL,
    office_address VARCHAR(255),
    ward_chairperson VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Tilottama Municipality Wards
INSERT INTO wards (ward_number, ward_name) VALUES
(1, 'Ward 1'),
(2, 'Ward 2'),
(3, 'Ward 3'),
(4, 'Ward 4'),
(5, 'Ward 5'),
(6, 'Ward 6'),
(7, 'Ward 7'),
(8, 'Ward 8'),
(9, 'Ward 9'),
(10, 'Ward 10'),
(11, 'Ward 11'),
(12, 'Ward 12'),
(13, 'Ward 13'),
(14, 'Ward 14'),
(15, 'Ward 15'),
(16, 'Ward 16'),
(17, 'Ward 17');

-- Verify Data
SELECT * FROM wards;