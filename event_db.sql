-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: event
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `event`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `event` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `event`;

--
-- Table structure for table `event_data`
--

DROP TABLE IF EXISTS `event_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_data` (
  `event_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_noun_id` int(11) NOT NULL,
  `event_rule_id` int(11) NOT NULL,
  `event_data_json_rep` json DEFAULT NULL,
  PRIMARY KEY (`event_data_id`),
  KEY `fk_event_data_1_idx` (`event_rule_id`),
  KEY `fk_event_data_2_idx` (`event_noun_id`),
  CONSTRAINT `fk_event_data_1` FOREIGN KEY (`event_rule_id`) REFERENCES `event_rule` (`event_rule_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_event_data_2` FOREIGN KEY (`event_noun_id`) REFERENCES `event_info` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `event_execute`
--

DROP TABLE IF EXISTS `event_execute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_execute` (
  `event_execute_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_rule_id` int(11) NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`event_execute_id`),
  KEY `fk_event_execute_temp_1_idx` (`event_rule_id`),
  CONSTRAINT `fk_event_execute_temp_1` FOREIGN KEY (`event_rule_id`) REFERENCES `event_rule` (`event_rule_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=163 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `event_info`
--

DROP TABLE IF EXISTS `event_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_info` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_noun` varchar(512) NOT NULL,
  PRIMARY KEY (`event_id`),
  UNIQUE KEY `event_noun_UNIQUE` (`event_noun`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `event_rule`
--

DROP TABLE IF EXISTS `event_rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_rule` (
  `event_rule_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_rule_name` varchar(512) NOT NULL,
  `event_rule_verb` varchar(512) NOT NULL,
  `event_rule_no_of_attempts` int(11) NOT NULL,
  `event_rule_time_interval` int(11) NOT NULL,
  `event_noun_id` int(11) NOT NULL,
  PRIMARY KEY (`event_rule_id`),
  UNIQUE KEY `event_rule_name_UNIQUE` (`event_rule_name`),
  UNIQUE KEY `event_rule_verb_UNIQUE` (`event_rule_verb`),
  KEY `fk_event_rule_1_idx` (`event_noun_id`),
  CONSTRAINT `fk_event_rule_1` FOREIGN KEY (`event_noun_id`) REFERENCES `event_info` (`event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-27 13:25:20
