-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 29, 2024 at 06:09 AM
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
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`user_id`, `user_name`, `user_dname`, `user_password`, `user_role`, `user_lastlogin`, `user_creation`) VALUES
(1, 'admin', 'admin', 'scrypt:32768:8:1$tigwUNjxpobIU2a9$00d9e2db5d6784952bac030bb4b2ec5f013b0dfc878dada7658835216fcb56d0286e35a0ec5d68bcd6f5f26889e641f849e523705bf71d301be73488340575a3', 'administrator', NULL, '2024-06-29 04:34:09');

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
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
  `paper_version` int NOT NULL,
  `paper_uploadedby` int NOT NULL,
  `paper_schedule_time` timestamp NOT NULL,
  `paper_expiry_time` timestamp NOT NULL,
  `paper_access` text NOT NULL,
  `paper_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`paper_id`),
  KEY `fk_paper_uploadedby` (`paper_uploadedby`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
