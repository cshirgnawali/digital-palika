USE digital_palika;

-- ===========================================
-- USERS TABLE
-- ===========================================

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin','mayor','staff','citizen') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- ===========================================
-- DEPARTMENTS TABLE
-- ===========================================

CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- ===========================================
-- WARDS TABLE
-- ===========================================

CREATE TABLE wards (
    ward_id INT AUTO_INCREMENT PRIMARY KEY,
    ward_number INT NOT NULL UNIQUE,
    ward_name VARCHAR(100) NOT NULL,
    office_address VARCHAR(255),
    ward_chairperson VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- ===========================================
-- PROJECTS TABLE
-- ===========================================

CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT NOT NULL,
    ward_id INT NOT NULL,
    project_name VARCHAR(200) NOT NULL,
    description TEXT,
    estimated_cost DECIMAL(15,2) NOT NULL,
    start_date DATE,
    expected_end_date DATE,
    status ENUM('Planned', 'Ongoing', 'Completed', 'Cancelled') DEFAULT 'Planned',
    contractor_name VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (ward_id) REFERENCES wards(ward_id)
);
-- ===========================================
-- BUDGETS TABLE
-- ===========================================

CREATE TABLE budgets (
    budget_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    fiscal_year VARCHAR(20) NOT NULL,
    allocated_amount DECIMAL(15,2) NOT NULL,
    spent_amount DECIMAL(15,2) DEFAULT 0.00,
    budget_status ENUM('Allocated', 'In Progress', 'Completed') DEFAULT 'Allocated',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);
-- ===========================================
-- COMPLAINTS TABLE
-- ===========================================

CREATE TABLE complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    department_id INT NOT NULL,
    ward_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255),
    priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    status ENUM('Pending', 'In Progress', 'Resolved', 'Rejected') DEFAULT 'Pending',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (ward_id) REFERENCES wards(ward_id)
);
-- ===========================================
-- COMPLAINT UPDATES TABLE
-- ===========================================

CREATE TABLE complaint_updates (
    update_id INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id INT NOT NULL,
    staff_id INT NOT NULL,
    status ENUM('Pending', 'In Progress', 'Resolved', 'Rejected') NOT NULL,
    remarks TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id),
    FOREIGN KEY (staff_id) REFERENCES users(user_id)
);
-- ===========================================
-- ANNOUNCEMENTS TABLE
-- ===========================================

CREATE TABLE announcements (
    announcement_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    published_by INT NOT NULL,
    publish_date DATE NOT NULL,
    expiry_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (published_by) REFERENCES users(user_id)
);
-- ===========================================
-- FEEDBACK TABLE
-- ===========================================

CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    rating INT NOT NULL,
    message TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
