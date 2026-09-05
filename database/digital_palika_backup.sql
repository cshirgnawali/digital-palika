-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: digital_palika
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `announcement_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `published_by` int NOT NULL,
  `publish_date` date NOT NULL,
  `expiry_date` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`announcement_id`),
  KEY `published_by` (`published_by`),
  CONSTRAINT `announcements_ibfk_1` FOREIGN KEY (`published_by`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` VALUES (1,'Property Tax Collection Notice','Citizens are requested to pay their property tax before the due date to avoid late payment penalties.',1,'2026-07-20','2026-08-31','2026-07-23 02:44:15'),(2,'Free Health Camp','Tilottama Municipality is organizing a free health camp for senior citizens at the Community Health Center.',1,'2026-07-22','2026-07-30','2026-07-23 02:44:15'),(3,'Road Maintenance Schedule','Road maintenance work will be carried out in Driver Tole and nearby areas. Please use alternative routes during construction.',1,'2026-07-25','2026-08-15','2026-07-23 02:44:15'),(4,'Water Supply Interruption','Water supply will remain suspended on Sunday from 9:00 AM to 3:00 PM due to pipeline maintenance.',1,'2026-07-24','2026-07-24','2026-07-23 02:44:15'),(5,'Digital Citizen Services','Citizens can now submit complaints, check project status, and access municipal services through the Digital Palika portal.',1,'2026-07-23','2026-12-31','2026-07-23 02:44:15'),(6,'Tree Plantation Program','Residents are invited to participate in the municipality-wide tree plantation campaign next Saturday.',1,'2026-07-28','2026-08-05','2026-07-23 02:44:15'),(7,'Test Announcement','Announcement of Test Example and Editable',133,'2026-12-11','2026-12-24','2026-07-25 15:12:14'),(8,'Monsoon Season Starting Very Soon','The monsoon season is starting very soon so the work will be delayed by sometime so please everyone dont be panic .. Thank you !!!',139,'2026-08-02','2026-11-12','2026-08-02 07:53:47'),(9,'Road Accident Reason','More than 40 percent road accidents are because of over speeding and due to not working of traffic signals properly , so we decided to make traffic fines higher if rule broken are found and we are upgrading the current version of traffic signal lights to the newest versions  ',139,'2026-08-02','2026-11-12','2026-08-02 08:28:56'),(10,'Drivertole Road Fixed ','The complaint made  from Shasank Pokhrel regarding the condition of road is fixed properly ',1,'2026-08-08','2026-08-09','2026-08-08 06:37:15');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `budgets`
--

DROP TABLE IF EXISTS `budgets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `budgets` (
  `budget_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `fiscal_year` varchar(20) NOT NULL,
  `allocated_amount` decimal(15,2) NOT NULL,
  `spent_amount` decimal(15,2) DEFAULT '0.00',
  `budget_status` enum('Allocated','In Progress','Completed') DEFAULT 'Allocated',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`budget_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `budgets_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `budgets`
--

LOCK TABLES `budgets` WRITE;
/*!40000 ALTER TABLE `budgets` DISABLE KEYS */;
INSERT INTO `budgets` VALUES (1,1,'2083/84',8500000.00,4500000.00,'In Progress','2026-07-23 02:34:03'),(2,2,'2083/84',6200000.00,500000.00,'Allocated','2026-07-23 02:34:03'),(3,3,'2083/84',1800000.00,900000.00,'In Progress','2026-07-23 02:34:03'),(4,4,'2083/84',9500000.00,7900000.00,'In Progress','2026-07-23 02:34:03'),(5,5,'2083/84',4300000.00,1200000.00,'Completed','2026-07-23 02:34:03'),(6,6,'2083/84',5200000.00,450000.00,'Allocated','2026-07-23 02:34:03'),(7,7,'2083/84',7100000.00,3600000.00,'In Progress','2026-07-23 02:34:03'),(8,8,'2083/84',3100000.00,123344.00,'Allocated','2026-07-23 02:34:03');
/*!40000 ALTER TABLE `budgets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaint_updates`
--

DROP TABLE IF EXISTS `complaint_updates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaint_updates` (
  `update_id` int NOT NULL AUTO_INCREMENT,
  `complaint_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `status` enum('Pending','In Progress','Resolved','Rejected') NOT NULL,
  `remarks` text,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`update_id`),
  KEY `complaint_id` (`complaint_id`),
  KEY `staff_id` (`staff_id`),
  CONSTRAINT `complaint_updates_ibfk_1` FOREIGN KEY (`complaint_id`) REFERENCES `complaints` (`complaint_id`) ON DELETE CASCADE,
  CONSTRAINT `complaint_updates_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaint_updates`
--

LOCK TABLES `complaint_updates` WRITE;
/*!40000 ALTER TABLE `complaint_updates` DISABLE KEYS */;
INSERT INTO `complaint_updates` VALUES (1,1,2,'In Progress','Engineering team has inspected the damaged road. Repair work will begin next week.','2026-07-23 02:41:38'),(2,2,3,'In Progress','Water supply pipeline inspection has been scheduled.','2026-07-23 02:41:38'),(3,3,2,'Pending','Complaint registered. Sanitation team will visit shortly.','2026-07-23 02:41:38'),(4,4,3,'Resolved','Free health camp conducted successfully for local residents.','2026-07-23 02:41:38'),(5,5,2,'In Progress','Roof renovation work has started.','2026-07-23 02:41:38'),(6,6,2,'Pending','Drainage cleaning team has been notified.','2026-07-23 02:41:38'),(7,7,3,'Resolved','Online tax payment portal issue fixed and verified.','2026-07-23 02:41:38'),(8,8,2,'Pending','Garbage collection vehicle assigned to the area.','2026-07-23 02:41:38');
/*!40000 ALTER TABLE `complaint_updates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaints`
--

DROP TABLE IF EXISTS `complaints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaints` (
  `complaint_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `department_id` int NOT NULL,
  `ward_id` int NOT NULL,
  `title` varchar(150) NOT NULL,
  `description` text NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `priority` enum('Low','Medium','High') DEFAULT 'Medium',
  `status` enum('Pending','In Progress','Resolved','Rejected') DEFAULT 'Pending',
  `submitted_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `citizen_name` varchar(100) DEFAULT NULL,
  `citizen_email` varchar(100) DEFAULT NULL,
  `submitted_date` date DEFAULT NULL,
  PRIMARY KEY (`complaint_id`),
  KEY `user_id` (`user_id`),
  KEY `department_id` (`department_id`),
  KEY `ward_id` (`ward_id`),
  CONSTRAINT `complaints_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `complaints_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`) ON DELETE CASCADE,
  CONSTRAINT `complaints_ibfk_3` FOREIGN KEY (`ward_id`) REFERENCES `wards` (`ward_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaints`
--

LOCK TABLES `complaints` WRITE;
/*!40000 ALTER TABLE `complaints` DISABLE KEYS */;
INSERT INTO `complaints` VALUES (1,4,2,1,'Road damaged after monsoon','The internal road has developed several potholes after heavy rainfall, making travel difficult.','Driver Tole, Ward 1','High','Pending','2026-07-23 02:36:18','Public Citizen',NULL,'2026-08-03'),(2,5,8,5,'Low water pressure','Residents are experiencing very low water pressure during the morning hours.','Manigram Chowk East, Ward 5','Medium','In Progress','2026-07-23 02:36:18','Public Citizen',NULL,'2026-08-03'),(3,6,6,9,'Garbage not collected','Household waste has not been collected for more than a week.','Kevalani, Ward 9','High','Pending','2026-07-23 02:36:18','Public Citizen',NULL,'2026-08-03'),(4,4,3,12,'Need additional health camp','The community has requested a free health check-up camp for senior citizens.','Makrahar, Ward 12','Low','Resolved','2026-07-23 02:36:18','Public Citizen',NULL,'2026-08-03'),(5,5,4,14,'School building roof leaking','Rainwater is leaking through the roof of the government school building.','Tikuligadh, Ward 14','High','Pending','2026-07-23 02:36:18','Public Citizen',NULL,'2026-08-03'),(6,6,2,15,'Blocked roadside drainage','Drainage is blocked, causing waterlogging during rainfall.','Kotihawa, Ward 15','Medium','Pending','2026-07-23 02:36:18','Public Citizen',NULL,'2026-08-03'),(7,4,9,6,'Online tax payment not working','Unable to submit property tax through the municipality portal.','Manigram, Ward 6','Medium','Resolved','2026-07-23 02:36:18','Public Citizen',NULL,'2026-08-03'),(8,5,6,13,'Overflowing public dustbin','The public dustbin has not been emptied and is overflowing.','Bisauriya, Ward 13','Low','Pending','2026-07-23 02:36:18','Public Citizen',NULL,'2026-08-03'),(17,1,2,11,'No work updated','work is not updated in the dashboards and notice boards okay','manigram','Medium','Pending','2026-07-25 11:18:25','Public Citizen',NULL,'2026-08-03'),(21,140,1,1,'ward work not done','no blacktopping is done on todays date',NULL,'Medium','Resolved','2026-08-02 16:01:28','Test Citizen','test@citizen.com','2026-08-02'),(23,140,1,3,'water problem','water problem is increasing day by day \r\n','None','Medium','In Progress','2026-08-02 16:02:17','Test Citizen','test@citizen.com','2026-08-02'),(24,140,1,1,'Water Level Rise in Tank','the water level in the tank is full and water still coming ,,, stop this as soon as possible ','main road , drivertole lumbini city college','Medium','Resolved','2026-08-03 12:16:44','Test Citizen','test@citizen.com','2026-08-03'),(26,148,1,1,'Street Light Not Working','Street lights have been off for 3 days.','Ward 3 Main Road','High','Resolved','2026-08-08 05:19:23','Shishir Gnawali','gnawalishishir53@gmail.com','2026-08-08'),(28,151,1,1,'Road Broken','road is not good looking , too much holes in the road','Drivertole, highway infront of lcc','Medium','Resolved','2026-08-08 06:32:35','Shasank Pokhrel','pokhrelshasank41@gmail.com','2026-08-08');
/*!40000 ALTER TABLE `complaints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `department_id` int NOT NULL AUTO_INCREMENT,
  `department_name` varchar(100) NOT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`department_id`),
  UNIQUE KEY `department_name` (`department_name`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'Administration','General administration and governance','2026-07-22 12:43:26'),(2,'Engineering','Roads, bridges, buildings and infrastructure','2026-07-22 12:43:26'),(3,'Health','Health services and public health','2026-07-22 12:43:26'),(4,'Education','Schools and educational programs','2026-07-22 12:43:26'),(5,'Revenue','Tax collection and municipal revenue','2026-07-22 12:43:26'),(6,'Sanitation','Waste management and sanitation','2026-07-22 12:43:26'),(7,'Agriculture','Agricultural development and farmer support','2026-07-22 12:43:26'),(8,'Water Supply','Water distribution and maintenance','2026-07-22 12:43:26'),(9,'Information Technology','Digital services and IT support','2026-07-22 12:43:26'),(45,'Tourism','Tourism promotion and cultural heritage management','2026-07-25 03:18:05');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `feedback_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `rating` int NOT NULL,
  `message` text NOT NULL,
  `submitted_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`feedback_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `feedback_chk_1` CHECK ((`rating` between 1 and 5))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,4,5,'The Digital Palika portal is very easy to use. I was able to submit my complaint without visiting the municipality office.','2026-07-23 02:47:03'),(2,5,4,'Road maintenance work in our ward was completed on time. Overall, I am satisfied with the municipal service.','2026-07-23 02:47:03'),(3,6,5,'My complaint regarding garbage collection was handled quickly. Thank you to the sanitation team.','2026-07-23 02:47:03'),(4,4,4,'The online property tax payment system is convenient and saves a lot of time.','2026-07-23 02:47:03'),(5,5,5,'The free health camp was well organized and very beneficial for senior citizens.','2026-07-23 02:47:03'),(6,6,4,'It would be helpful if more municipal services were available online, but the current system works well.','2026-07-23 02:47:03');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_updates`
--

DROP TABLE IF EXISTS `project_updates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_updates` (
  `update_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `update_text` varchar(255) NOT NULL,
  `update_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`update_id`),
  KEY `project_id` (`project_id`),
  KEY `staff_id` (`staff_id`),
  CONSTRAINT `project_updates_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `project_updates_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_updates`
--

LOCK TABLES `project_updates` WRITE;
/*!40000 ALTER TABLE `project_updates` DISABLE KEYS */;
INSERT INTO `project_updates` VALUES (1,8,139,'Pipe installation completed up to Ward 10 eastern section.\r\nWater flow testing will begin tomorrow.','2026-07-31 09:56:27'),(2,6,139,'finished \r\n','2026-08-08 06:13:46');
/*!40000 ALTER TABLE `project_updates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `project_id` int NOT NULL AUTO_INCREMENT,
  `department_id` int NOT NULL,
  `ward_id` int NOT NULL,
  `project_name` varchar(200) NOT NULL,
  `description` text,
  `estimated_cost` decimal(15,2) NOT NULL,
  `start_date` date DEFAULT NULL,
  `expected_end_date` date DEFAULT NULL,
  `status` enum('Planned','Ongoing','Completed','Cancelled') DEFAULT 'Planned',
  `contractor_name` varchar(150) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `priority` enum('Low','Medium','High') DEFAULT 'Medium',
  `mayor_remark` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`project_id`),
  KEY `department_id` (`department_id`),
  KEY `ward_id` (`ward_id`),
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`) ON DELETE CASCADE,
  CONSTRAINT `projects_ibfk_2` FOREIGN KEY (`ward_id`) REFERENCES `wards` (`ward_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,2,1,'Road Blacktopping - Driver Tole','Blacktopping of internal roads in Driver Tole.',8500000.00,'2026-07-01','2026-11-30','Ongoing','Shrestha Construction Pvt. Ltd.','2026-07-23 02:31:52','Medium',NULL),(2,8,5,'Water Supply Pipeline Expansion','Extension of drinking water pipelines in Ward 5.',6200000.00,'2026-08-01','2026-12-15','Planned','Lumbini Water Works','2026-07-23 02:31:52','Medium',NULL),(3,6,9,'Solid Waste Management Program','Installation of waste collection bins and awareness campaign.',1800000.00,'2026-06-15','2026-09-30','Ongoing','Green Nepal Services','2026-07-23 02:31:52','Medium',NULL),(4,3,12,'Community Health Center Upgrade','Expansion of health center building and medical equipment.',9500000.00,'2026-05-01','2026-10-31','Ongoing','Everest Builders','2026-07-23 02:31:52','Medium',NULL),(5,4,14,'School Building Renovation','Renovation of government school classrooms.',4300000.00,'2026-04-10','2026-07-20','Completed','ABC Engineering 1','2026-07-23 02:31:52','Medium',NULL),(6,9,6,'Municipality Digital Service Center','Development of digital citizen service center.',5200000.00,'2026-08-10','2027-01-15','Completed','Tech Solutions Nepal','2026-07-23 02:31:52','High','Complete this task fast ! \r\n'),(7,2,15,'Drainage Construction Project','Construction of roadside drainage system.',7100000.00,'2026-06-20','2026-12-20','Ongoing','Buddha Construction','2026-07-23 02:31:52','Medium',NULL),(8,7,13,'Agriculture Training Center','Training center for modern farming techniques.',3100000.00,'2026-07-15','2026-10-15','Completed','Rural Development Nepal','2026-07-23 02:31:52','Medium',NULL),(9,5,10,'Water Supply Related','provide water supplies to public',400000.61,'2025-12-11','2026-12-11','Planned','Regmi Constructions','2026-07-25 10:18:41','Medium','the weather is normal now ');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `mobile_number` varchar(15) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','mayor','staff','citizen') NOT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `mobile_number` (`mobile_number`)
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Admin User',NULL,'admin@tilottama.gov.np','9800000001','scrypt:32768:8:1$zjYNKuIfnlEFuCdW$3aa1aa70836024bec61114e496b51b5ee5276d365fb715320bd0e02f9517514ff9ed39d503f33af39ff2c26c268c63b1fe48e5d19d280857ac70b7dd3ba6ebfa','admin','active','2026-07-22 13:10:41'),(2,'Ram Bahadur Thapa',NULL,'ram@tilottama.gov.np','9800000002','scrypt:32768:8:1$4mL5ncVaP0miyd9F$b2a0d6b3e1915d4bdc11d3d9c4f750eaab42ed4fd9b315c12300db12674a16faeacde4af20df361cfaadaefb38dc3c1e0bbe728d9aabca98dfb2bd060e2452b9','staff','active','2026-07-22 13:10:41'),(3,'Sita Sharma',NULL,'sita@tilottama.gov.np','9800000003','scrypt:32768:8:1$4mL5ncVaP0miyd9F$b2a0d6b3e1915d4bdc11d3d9c4f750eaab42ed4fd9b315c12300db12674a16faeacde4af20df361cfaadaefb38dc3c1e0bbe728d9aabca98dfb2bd060e2452b9','staff','active','2026-07-22 13:10:41'),(4,'Hari Prasad Gautam',NULL,'hari@gmail.com','9811111111','scrypt:32768:8:1$JvUW3BkCZ97cjt71$5cfb46c49bf6f6a1a47964f325cb2d88b9739396633cafbbf230498f255e9706d57defb8b7c373583602b9b9b01ad82e8682565c34012752b0015d094aa91e01','citizen','active','2026-07-22 13:10:41'),(5,'Anita Karki',NULL,'anita@gmail.com','9822222222','scrypt:32768:8:1$JvUW3BkCZ97cjt71$5cfb46c49bf6f6a1a47964f325cb2d88b9739396633cafbbf230498f255e9706d57defb8b7c373583602b9b9b01ad82e8682565c34012752b0015d094aa91e01','citizen','active','2026-07-22 13:10:41'),(6,'Ramesh Bhandari',NULL,'ramesh@gmail.com','9833333333','scrypt:32768:8:1$JvUW3BkCZ97cjt71$5cfb46c49bf6f6a1a47964f325cb2d88b9739396633cafbbf230498f255e9706d57defb8b7c373583602b9b9b01ad82e8682565c34012752b0015d094aa91e01','citizen','active','2026-07-22 13:10:41'),(133,'Khadga Prasad Acharya',NULL,'mayor@tilottama.gov.np','9800000004','scrypt:32768:8:1$eFX02M1vwhWLwtjp$263025f8547fae0b7b89667ed1b3d5b63c0a23b9ebb03d2026140412359ae102f8ab7f100811f80176b60c3bd4fa26f3f6ff86567c530e912bff1ddae0ca0d52','mayor','active','2026-07-23 09:56:41'),(136,'Prabesh Xetri',NULL,'prabesh@xetri.gov.np','9867812737','scrypt:32768:8:1$T0Vk1YcbiclIcIpO$3341fbb0ac8038d4ee476f8d396417f89d060b0602790857e14266b24efd83e0116573fe51f5773023b878282a4e717c32e62c8d0edb54a142514064eb2cfd16','citizen','active','2026-07-27 01:00:37'),(137,'Test User',NULL,'test@examples.com','9867813737','scrypt:32768:8:1$dNmMe9RtXEQdYHmM$350db4dc40e745bd151b05ba7c0f60bc4c56234a1cdae1d72c438178f25c0391be28bc02fd58960d97d1a40f03b110e5648f6fbaecdc258650d3462c415423df','citizen','active','2026-07-28 12:11:51'),(138,'Test Mayor',NULL,'test@mayor.com','9812312312','scrypt:32768:8:1$tdymLaDkUJoXIzOd$af67a8e46c9787800ba96dc4209805f95b80fc9aa13a934b958a85495cc23080bf26008c6a0d062334f964ae7325c6be9f5f60bb956766802eb88c146b944d28','mayor','active','2026-07-29 07:07:59'),(139,'Test Staff',NULL,'test@staff.com','9812345678','scrypt:32768:8:1$PxjnOdkyXfp5YKPM$ae124e9e31a4ec3b003698fae0cb49f3110249eea2e9cf6cf164688662f7b7d455eda9eb0f06f85be0d116db32b20eec3ef56a2f2fa95216b3c8f72f37bf394b','staff','active','2026-07-30 12:12:41'),(140,'Test Citizen',NULL,'test@citizen.com','9812345678','scrypt:32768:8:1$rHGuk06NajCdu8kY$fac84eec08ad3c7793cf8829a2eb68c68cff6c1d08f7614afec1b831ba2a4a9db487b822b5692a7326450184f36e7896ad124fc74d0bf074e4278be990baf230','citizen','active','2026-08-02 09:56:27'),(148,'Shishir Gnawali','9746399853','gnawalishishir53@gmail.com','9746399853','scrypt:32768:8:1$dWsYsLtWtRBuaXp4$e0a362665770c557085d643147a3d9ee86970c51755f3ece88e516445d532991be3fc9c60bbe8b7b1fd7311593b0e7a005400109750d169a517ee314c81302e0','citizen','active','2026-08-08 04:29:07'),(150,'Test Mayor 2',NULL,'test@mayor2.com','9800000006','scrypt:32768:8:1$X373cs3TEBty2npq$eb318511418ce6d0a9f3abca78fc497b09ec1733a85a5bd591c92049f5ddaf51987375d6488d662818aafad8ae5db843013f6d6780604dcd72cf18f98961c1ab','mayor','active','2026-08-08 04:42:59'),(151,'Shasank Pokhrel','9867932176','pokhrelshasank41@gmail.com','9867932176','scrypt:32768:8:1$Iyfplb65LjErQnT6$fd2ea4f41f4e0c6e9595581e53fd7569ea4630851c976158f45aa90d995b346b00134895f862d16d3f90464ac2c47e6fc7023af3258e152d7863a08cefc1f247','citizen','active','2026-08-08 06:30:51');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wards`
--

DROP TABLE IF EXISTS `wards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wards` (
  `ward_id` int NOT NULL AUTO_INCREMENT,
  `ward_number` int NOT NULL,
  `ward_name` varchar(100) NOT NULL,
  `office_address` varchar(255) DEFAULT NULL,
  `ward_chairperson` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ward_id`),
  UNIQUE KEY `ward_number` (`ward_number`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wards`
--

LOCK TABLES `wards` WRITE;
/*!40000 ALTER TABLE `wards` DISABLE KEYS */;
INSERT INTO `wards` VALUES (1,1,'Driver Tole','Tilottama Municipality Ward Office 1','Farsu Ram Giri','2026-07-22 12:42:25'),(2,2,'Shankarnagar','Tilottama Municipality Ward Office 2','Dil Bahadur Bhattarai','2026-07-22 12:42:25'),(3,3,'Janakinagar','Tilottama Municipality Ward Office 3','Kalyan Prasad Poudel','2026-07-22 12:42:25'),(4,4,'Dingarnagar','Tilottama Municipality Ward Office 4','Hari Bahadur Kshetri','2026-07-22 12:42:25'),(5,5,'Manigram Chowk East','Tilottama Municipality Ward Office 5','Ramesh Dumre','2026-07-22 12:42:25'),(6,6,'Manigram','Tilottama Municipality Ward Office 6','Ganesh Pathak','2026-07-22 12:42:25'),(7,7,'Kevalani','Tilottama Municipality Ward Office 7','Devi Prasad Pangeni','2026-07-22 12:42:25'),(8,8,'Jyotinagar','Tilottama Municipality Ward Office 8','Krishna Prasad Poudel','2026-07-22 12:42:25'),(9,9,'Kevalani','Tilottama Municipality Ward Office 9','Dhruva Nyaupane','2026-07-22 12:42:25'),(10,10,'Bebari','Tilottama Municipality Ward Office 10','Gopal Prasad Ghimire','2026-07-22 12:42:25'),(11,11,'Madrahani','Tilottama Municipality Ward Office 11','Bishnu Bahadur Baral Kshetri','2026-07-22 12:42:25'),(12,12,'Makrahar','Tilottama Municipality Ward Office 12','Sahadev Tharu','2026-07-22 12:42:25'),(13,13,'Bisauriya','Tilottama Municipality Ward Office 13','Narayan Dhakal','2026-07-22 12:42:25'),(14,14,'Tikuligadh','Tilottama Municipality Ward Office 14','Ashwin Poudel','2026-07-22 12:42:25'),(15,15,'Kotihawa','Tilottama Municipality Ward Office 15','Khemraj Gurung','2026-07-22 12:42:25'),(16,16,'Judwa','Tilottama Municipality Ward Office 16','Jhabilal Bhusal','2026-07-22 12:42:25'),(17,17,'Gangoliya','Tilottama Municipality Ward Office 17','Dan Bahadur Chaudhary','2026-07-22 12:42:25');
/*!40000 ALTER TABLE `wards` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-08 20:35:40
