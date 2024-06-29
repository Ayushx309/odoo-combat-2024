-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 29, 2024 at 02:31 PM
-- Server version: 8.2.0
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `spds`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
CREATE TABLE IF NOT EXISTS `accounts` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(256) NOT NULL,
  `user_dname` varchar(256) NOT NULL,
  `user_password` varchar(256) NOT NULL,
  `user_role` enum('administrator','examiner','invigilator') NOT NULL,
  `user_lastlogin` timestamp NULL DEFAULT NULL,
  `user_creation` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`user_id`, `user_name`, `user_dname`, `user_password`, `user_role`, `user_lastlogin`, `user_creation`) VALUES
(1, 'admin', 'admin', 'scrypt:32768:8:1$tigwUNjxpobIU2a9$00d9e2db5d6784952bac030bb4b2ec5f013b0dfc878dada7658835216fcb56d0286e35a0ec5d68bcd6f5f26889e641f849e523705bf71d301be73488340575a3', 'administrator', '2024-06-29 14:17:18', '2024-06-29 04:34:09'),
(6, 'examiner', 'examiner', 'scrypt:32768:8:1$1El5zXTcbw6RolBx$36a3904cd38074c1ec4ba15c65d2559eedf23f821c550235829f41be9d1695d03fa5b41f7f1464271ab5f8b0fe4da84c2768f0114a0761dba6a0002205831baf', 'examiner', '2024-06-29 14:17:03', '2024-06-29 08:22:52'),
(7, 'tushar12', 'tushar khatri', 'scrypt:32768:8:1$bF8kgVa4AxSl30ZS$16417515d19b5d98c5c189c8847c003a8490c9ed38e4f31661d4ea6dc009f98e1150b38c2c24695cb9e5fd578032f3070aedee7f718faf863456d0b2e8ea20be', 'examiner', NULL, '2024-06-29 11:33:34'),
(8, 'ayushx309', 'Ayush Joshi', 'scrypt:32768:8:1$Vezh8ZIPkUWAcebz$08354b9bb76c1de14afda1bee7a086fe6937ee96c42287c896f2ba8f598e024a43e9881603aecbaffef5e2bccd74eda88357100b757524535c28c8bf7648162d', 'invigilator', '2024-06-29 14:18:55', '2024-06-29 11:33:51');

-- --------------------------------------------------------

--
-- Table structure for table `audit`
--

DROP TABLE IF EXISTS `audit`;
CREATE TABLE IF NOT EXISTS `audit` (
  `audit_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `audit_type` enum('login','access') NOT NULL,
  `paper_id` int DEFAULT NULL,
  `audit_action` enum('view','download') DEFAULT NULL,
  `audit_ip` varchar(256) NOT NULL,
  `audit_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`audit_id`),
  KEY `fk_user_id` (`user_id`),
  KEY `fk_paper_id` (`paper_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `audit`
--

INSERT INTO `audit` (`audit_id`, `user_id`, `audit_type`, `paper_id`, `audit_action`, `audit_ip`, `audit_timestamp`) VALUES
(1, 6, 'login', NULL, NULL, '127.0.0.1', '2024-06-29 13:21:17'),
(2, 7, 'login', NULL, NULL, '127.0.0.1', '2024-06-29 13:23:19'),
(3, 1, 'login', NULL, NULL, '127.0.0.1', '2024-06-29 13:24:52'),
(4, 8, 'login', NULL, NULL, '127.0.0.1', '2024-06-29 13:44:59'),
(5, 1, 'login', NULL, NULL, '127.0.0.1', '2024-06-29 13:45:04'),
(6, 6, 'login', NULL, NULL, '127.0.0.1', '2024-06-29 14:13:21'),
(7, 1, 'login', NULL, NULL, '127.0.0.1', '2024-06-29 14:17:08'),
(8, 8, 'login', NULL, NULL, '127.0.0.1', '2024-06-29 14:17:25'),
(9, 1, 'login', NULL, NULL, '127.0.0.1', '2024-06-29 14:19:01');

-- --------------------------------------------------------

--
-- Table structure for table `papers`
--

DROP TABLE IF EXISTS `papers`;
CREATE TABLE IF NOT EXISTS `papers` (
  `paper_id` int NOT NULL AUTO_INCREMENT,
  `paper_name` varchar(256) NOT NULL,
  `paper_desc` varchar(256) NOT NULL,
  `paper_path` text NOT NULL,
  `paper_password` text NOT NULL,
  `paper_version` int NOT NULL,
  `paper_uploadedby` int NOT NULL,
  `paper_schedule_time` timestamp NOT NULL,
  `paper_expiry_time` timestamp NOT NULL,
  `paper_access` text NOT NULL,
  `paper_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`paper_id`),
  KEY `fk_paper_uploadedby` (`paper_uploadedby`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `papers`
--

INSERT INTO `papers` (`paper_id`, `paper_name`, `paper_desc`, `paper_path`, `paper_password`, `paper_version`, `paper_uploadedby`, `paper_schedule_time`, `paper_expiry_time`, `paper_access`, `paper_timestamp`) VALUES
(2, 'Physics', 'good', 'Storage/papers/1719660540_56b62d6d.pdf', '<C:Vh9DaLVs.', 1, 1, '2024-06-30 06:30:00', '2024-06-30 06:35:00', '[1,6]', '2024-06-29 11:29:03'),
(3, 'Maths', 'Maths 12th', 'Storage/papers/1719660988_f0d6fa23.pdf', 'B,,.$ErTB[8A', 1, 6, '2024-07-01 06:30:00', '2024-07-02 06:30:00', '[1,7]', '2024-06-29 11:36:28'),
(4, 'CS', 'CS paper', 'Storage/papers/1719661031_afaf957c.pdf', '4x!(%!9Eio+r', 1, 6, '2024-07-03 06:30:00', '2024-07-03 09:30:00', '[8,6]', '2024-06-29 11:37:12'),
(5, 'Demo test', 'test', 'Storage/papers/1719665116_1660e939.pdf', '+=oZ;|}1u``R', 1, 6, '2024-06-30 06:30:00', '2024-06-30 06:30:00', '[8,7,6]', '2024-06-29 12:45:16'),
(6, 'test', 'test', 'Storage/papers/1719669342_b5a4bf0a.pdf', 'Cn%NXBu(j].-', 1, 1, '2024-06-29 06:30:00', '2024-06-30 06:30:00', '[1,6,8]', '2024-06-29 13:55:42');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
