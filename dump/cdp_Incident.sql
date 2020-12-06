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
-- Table structure for table `Incident`
--

DROP TABLE IF EXISTS `Incident`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Incident` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(100) NOT NULL,
  `incident_date` date NOT NULL,
  `incident_img` varchar(100) DEFAULT NULL,
  `created_on` datetime(6) NOT NULL,
  `created_by` varchar(20) NOT NULL,
  `modified_on` datetime(6) DEFAULT NULL,
  `modified_by` varchar(20) NOT NULL,
  `agent_id` int(11) NOT NULL,
  `mac_id` varchar(30) DEFAULT NULL,
  `notification_status` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Incident_agent_id_5c186ee4_fk_Agent_id` (`agent_id`),
  CONSTRAINT `Incident_agent_id_5c186ee4_fk_Agent_id` FOREIGN KEY (`agent_id`) REFERENCES `Agent` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Incident`
--

LOCK TABLES `Incident` WRITE;
/*!40000 ALTER TABLE `Incident` DISABLE KEYS */;
INSERT INTO `Incident` VALUES (1,'Camera Tampered','2020-06-26','NYC.jpg','2020-06-26 16:02:16.000000','Shyena Tech','2020-07-01 07:10:39.336399','Shyena Tech',1,'9999.8888.2222','Viewed'),(2,'Camera Tampered','2020-06-29','NYC.jpg','2020-06-29 18:47:17.000000','Shyena Tech','2020-06-29 18:47:17.000000','Shyena Tech',2,'9999.8.2222','Open'),(3,'Camera Tampered','2020-06-29','NYC.jpg','2020-06-29 18:59:22.000000','Shyena Tech','2020-06-29 18:59:22.000000','Shyena Tech',3,'922','Open');
/*!40000 ALTER TABLE `Incident` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-03 16:12:20
