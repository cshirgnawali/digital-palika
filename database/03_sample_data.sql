USE digital_palika;

-- ===========================================
-- USERS
-- ===========================================

INSERT INTO users (full_name, email, phone, password, role)
VALUES
('Admin User', 'admin@tilottama.gov.np', '9800000001', 'admin123', 'admin'),
('Khadga Prasad Acharya', 'mayor@tilottama.gov.np', '9800000004', 'mayor123', 'mayor'),
('Ram Bahadur Thapa', 'ram@tilottama.gov.np', '9800000002', 'staff123', 'staff'),
('Sita Sharma', 'sita@tilottama.gov.np', '9800000003', 'staff123', 'staff'),
('Hari Prasad Gautam', 'hari@gmail.com', '9811111111', 'citizen123', 'citizen'),
('Anita Karki', 'anita@gmail.com', '9822222222', 'citizen123', 'citizen'),
('Ramesh Bhandari', 'ramesh@gmail.com', '9833333333', 'citizen123', 'citizen');


-- ===========================================
-- DEPARTMENTS
-- ===========================================

INSERT INTO departments (department_name, description)
VALUES
('Administration', 'General administration and governance'),
('Engineering', 'Roads, bridges, buildings and infrastructure'),
('Health', 'Health services and public health'),
('Education', 'Schools and educational programs'),
('Revenue', 'Tax collection and municipal revenue'),
('Sanitation', 'Waste management and sanitation'),
('Agriculture', 'Agricultural development and farmer support'),
('Water Supply', 'Water distribution and maintenance'),
('Information Technology', 'Digital services and IT support');


-- ===========================================
-- WARDS
-- ===========================================

INSERT INTO wards (
    ward_number,
    ward_name,
    office_address,
    ward_chairperson
)
VALUES
(1, 'Driver Tole', 'Tilottama Municipality Ward Office 1', 'Farsu Ram Giri'),
(2, 'Shankarnagar', 'Tilottama Municipality Ward Office 2', 'Dil Bahadur Bhattarai'),
(3, 'Janakinagar', 'Tilottama Municipality Ward Office 3', 'Kalyan Prasad Poudel'),
(4, 'Dingarnagar', 'Tilottama Municipality Ward Office 4', 'Hari Bahadur Kshetri'),
(5, 'Manigram Chowk East', 'Tilottama Municipality Ward Office 5', 'Ramesh Dumre'),
(6, 'Manigram', 'Tilottama Municipality Ward Office 6', 'Ganesh Pathak'),
(7, 'Kevalani', 'Tilottama Municipality Ward Office 7', 'Devi Prasad Pangeni'),
(8, 'Jyotinagar', 'Tilottama Municipality Ward Office 8', 'Krishna Prasad Poudel'),
(9, 'Kevalani', 'Tilottama Municipality Ward Office 9', 'Dhruva Nyaupane'),
(10, 'Bebari', 'Tilottama Municipality Ward Office 10', 'Gopal Prasad Ghimire'),
(11, 'Madrahani', 'Tilottama Municipality Ward Office 11', 'Bishnu Bahadur Baral Kshetri'),
(12, 'Makrahar', 'Tilottama Municipality Ward Office 12', 'Sahadev Tharu'),
(13, 'Bisauriya', 'Tilottama Municipality Ward Office 13', 'Narayan Dhakal'),
(14, 'Tikuligadh', 'Tilottama Municipality Ward Office 14', 'Ashwin Poudel'),
(15, 'Kotihawa', 'Tilottama Municipality Ward Office 15', 'Khemraj Gurung'),
(16, 'Judwa', 'Tilottama Municipality Ward Office 16', 'Jhabilal Bhusal'),
(17, 'Gangoliya', 'Tilottama Municipality Ward Office 17', 'Dan Bahadur Chaudhary');
-- ===========================================
-- PROJECTS
-- ===========================================

INSERT INTO projects (
    department_id,
    ward_id,
    project_name,
    description,
    estimated_cost,
    start_date,
    expected_end_date,
    status,
    contractor_name
)
VALUES
(2, 1, 'Road Blacktopping - Driver Tole',
'Blacktopping of internal roads in Driver Tole.',
8500000.00, '2026-07-01', '2026-12-30', 'Ongoing', 'Sharma Construction Pvt. Ltd.'),

(8, 5, 'Water Supply Pipeline Expansion',
'Extension of drinking water pipelines in Ward 5.',
6200000.00, '2026-08-01', '2027-01-15', 'Planned', 'Lumbini Water Engineering'),

(6, 9, 'Solid Waste Management Program',
'Installation of waste collection bins and awareness campaign.',
1800000.00, '2026-06-15', '2026-09-30', 'Ongoing', 'Clean Nepal Services'),

(3, 12, 'Community Health Center Upgrade',
'Expansion of health center building and medical equipment.',
9500000.00, '2026-05-10', '2026-11-20', 'Ongoing', 'Everest Builders'),

(4, 14, 'School Building Renovation',
'Renovation of government school classrooms.',
4300000.00, '2026-04-01', '2026-07-15', 'Completed', 'ABC Construction'),

(9, 6, 'Municipality Digital Service Center',
'Development of digital citizen service center.',
5200000.00, '2026-08-15', '2027-02-15', 'Planned', 'Tech Solutions Nepal'),

(2, 15, 'Drainage Construction Project',
'Construction of roadside drainage system.',
7100000.00, '2026-06-01', '2026-11-30', 'Ongoing', 'Lumbini Infrastructure'),

(7, 13, 'Agriculture Training Center',
'Training center for modern farming techniques.',
3100000.00, '2026-09-01', '2027-01-30', 'Planned', 'Agro Nepal Pvt. Ltd.');


-- ===========================================
-- BUDGETS
-- ===========================================

INSERT INTO budgets (
    project_id,
    fiscal_year,
    allocated_amount,
    spent_amount,
    budget_status
)
VALUES
(1, '2083/84', 8500000.00, 4200000.00, 'In Progress'),
(2, '2083/84', 6200000.00, 0.00, 'Allocated'),
(3, '2083/84', 1800000.00, 900000.00, 'In Progress'),
(4, '2083/84', 9500000.00, 7800000.00, 'In Progress'),
(5, '2083/84', 4300000.00, 4300000.00, 'Completed'),
(6, '2083/84', 5200000.00, 0.00, 'Allocated'),
(7, '2083/84', 7100000.00, 3600000.00, 'In Progress'),
(8, '2083/84', 3100000.00, 0.00, 'Allocated');
-- ===========================================
-- COMPLAINTS
-- ===========================================

INSERT INTO complaints (
    user_id,
    department_id,
    ward_id,
    title,
    description,
    location,
    priority,
    status
)
VALUES
(4, 2, 1,
'Road damaged after monsoon',
'The internal road has developed several potholes after heavy rainfall, making travel difficult.',
'Driver Tole, Ward 1',
'High',
'In Progress'),

(5, 8, 5,
'Low water pressure',
'Residents are experiencing very low water pressure during the morning hours.',
'Manigram Chowk East, Ward 5',
'Medium',
'Pending'),

(6, 6, 9,
'Garbage not collected',
'Household waste has not been collected for more than a week.',
'Kevalani, Ward 9',
'High',
'Pending'),

(4, 3, 12,
'Need additional health camp',
'The community has requested a free health check-up camp for senior citizens.',
'Makrahar, Ward 12',
'Medium',
'Resolved'),

(5, 4, 14,
'School building roof leaking',
'Rainwater is leaking through the roof of the government school building.',
'Tikuligadh, Ward 14',
'High',
'In Progress'),

(6, 2, 15,
'Blocked roadside drainage',
'Drainage is blocked, causing waterlogging during rainfall.',
'Kotihawa, Ward 15',
'Medium',
'Pending'),

(4, 9, 6,
'Online tax payment not working',
'Unable to submit property tax through the municipality portal.',
'Municipality Office',
'High',
'Resolved'),

(5, 6, 13,
'Overflowing public dustbin',
'The public dustbin has not been emptied and is overflowing.',
'Bisauriya, Ward 13',
'Medium',
'Pending');


-- ===========================================
-- COMPLAINT UPDATES
-- ===========================================

INSERT INTO complaint_updates (
    complaint_id,
    staff_id,
    status,
    remarks
)
VALUES
(1, 2, 'In Progress',
'Engineering team has inspected the damaged road. Repair work will begin next week.'),

(2, 3, 'In Progress',
'Water supply pipeline inspection has been scheduled.'),

(3, 2, 'Pending',
'Complaint registered. Sanitation team will visit shortly.'),

(4, 3, 'Resolved',
'Free health camp conducted successfully for local residents.'),

(5, 2, 'In Progress',
'Roof renovation work has started.'),

(6, 2, 'Pending',
'Drainage cleaning team has been notified.'),

(7, 3, 'Resolved',
'Online tax payment portal issue fixed and verified.'),

(8, 2, 'Pending',
'Garbage collection vehicle assigned to the area.');
-- ===========================================
-- ANNOUNCEMENTS
-- ===========================================

INSERT INTO announcements (
    title,
    description,
    published_by,
    publish_date,
    expiry_date
)
VALUES
(
'Property Tax Collection Notice',
'Citizens are requested to pay their property tax before the due date to avoid late payment penalties.',
1,
'2026-07-20',
'2026-08-20'
),
(
'Free Health Camp',
'Tilottama Municipality is organizing a free health camp for senior citizens at the Community Health Center.',
1,
'2026-07-22',
'2026-07-30'
),
(
'Road Maintenance Schedule',
'Road maintenance work will be carried out in Driver Tole and nearby areas. Please use alternative routes during construction.',
1,
'2026-07-25',
'2026-08-10'
),
(
'Water Supply Interruption',
'Water supply will remain suspended on Sunday from 9:00 AM to 3:00 PM due to pipeline maintenance.',
1,
'2026-07-24',
'2026-07-24'
),
(
'Digital Citizen Services',
'Citizens can now submit complaints, check project status, and access municipal services through the Digital Palika portal.',
1,
'2026-07-23',
'2026-12-31'
),
(
'Tree Plantation Program',
'Residents are invited to participate in the municipality-wide tree plantation campaign next Saturday.',
1,
'2026-07-28',
'2026-08-05'
);


-- ===========================================
-- FEEDBACK
-- ===========================================

INSERT INTO feedback (
    user_id,
    rating,
    message
)
VALUES
(
4,
5,
'The Digital Palika portal is very easy to use. I was able to submit my complaint without visiting the municipality office.'
),
(
5,
4,
'Road maintenance work in our ward was completed on time. Overall, I am satisfied with the municipal service.'
),
(
6,
5,
'My complaint regarding garbage collection was handled quickly. Thank you to the sanitation team.'
),
(
4,
4,
'The online property tax payment system is convenient and saves a lot of time.'
),
(
5,
5,
'The free health camp was well organized and very beneficial for senior citizens.'
),
(
6,
4,
'It would be helpful if more municipal services were available online, but the current system works well.'
);
