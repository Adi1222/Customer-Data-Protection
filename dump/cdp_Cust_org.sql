-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: cdp
-- ------------------------------------------------------
-- Server version	5.7.30-0ubuntu0.18.04.1

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
-- Table structure for table `Cust_org`
--

DROP TABLE IF EXISTS `Cust_org`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cust_org` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_org` varchar(50) NOT NULL,
  `cust_org_acro` varchar(15) NOT NULL,
  `onboard_date` date NOT NULL,
  `status` varchar(10) NOT NULL,
  `is_deleted` varchar(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `created_by` varchar(20) NOT NULL,
  `modified_on` datetime(6) DEFAULT NULL,
  `modified_by` varchar(20) NOT NULL,
  `bill_plan_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cust_org` (`cust_org`),
  KEY `Cust_org_bill_plan_id_ccc58bfd_fk_Bill_plan_id` (`bill_plan_id`),
  CONSTRAINT `Cust_org_bill_plan_id_ccc58bfd_fk_Bill_plan_id` FOREIGN KEY (`bill_plan_id`) REFERENCES `Bill_plan` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cust_org`
--

LOCK TABLES `Cust_org` WRITE;
/*!40000 ALTER TABLE `Cust_org` DISABLE KEYS */;
INSERT INTO `Cust_org` VALUES (1,'Pantaloons','PPL','2020-05-05','Active','N','2020-05-05 11:48:45.066711','','2020-05-05 11:49:25.934611','',1),(2,'Westside','WS','2020-05-05','Active','N','2020-05-05 11:50:02.927647','','2020-05-13 12:03:24.055050','',1),(3,'Shyena Tech Yarns','STY','2020-05-05','Active','N','2020-05-05 13:31:23.817644','','2020-05-05 13:32:03.498537','',1);
/*!40000 ALTER TABLE `Cust_org` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-03 16:12:19
