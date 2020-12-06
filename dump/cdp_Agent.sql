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
-- Table structure for table `Agent`
--

DROP TABLE IF EXISTS `Agent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Agent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(15) NOT NULL,
  `lname` varchar(20) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `created_by` varchar(20) NOT NULL,
  `modified_on` datetime(6) DEFAULT NULL,
  `modified_by` varchar(20) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `lead_id` int(11) NOT NULL,
  `is_deleted` varchar(1) NOT NULL DEFAULT 'N',
  `manager_id` int(11) DEFAULT NULL,
  `mac_id` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Agent_customer_id_494363d4_fk_Cust_org_id` (`customer_id`),
  KEY `Agent_lead_id_a5799541_fk_Appuser_id` (`lead_id`),
  CONSTRAINT `Agent_customer_id_494363d4_fk_Cust_org_id` FOREIGN KEY (`customer_id`) REFERENCES `Cust_org` (`id`),
  CONSTRAINT `Agent_ibfk_1` FOREIGN KEY (`id`) REFERENCES `Appuser` (`id`) ON DELETE CASCADE,
  CONSTRAINT `Agent_lead_id_a5799541_fk_Appuser_id` FOREIGN KEY (`lead_id`) REFERENCES `Appuser` (`id`),
  CONSTRAINT `FK_Agent_man_id` FOREIGN KEY (`id`) REFERENCES `Appuser` (`id`),
  CONSTRAINT `FK_Agent_manager` FOREIGN KEY (`id`) REFERENCES `Appuser` (`id`),
  CONSTRAINT `FK_Agent_manager_id` FOREIGN KEY (`id`) REFERENCES `Appuser` (`id`),
  CONSTRAINT `FK_Agent_mang_id` FOREIGN KEY (`id`) REFERENCES `Appuser` (`id`),
  CONSTRAINT `FK_manager_id` FOREIGN KEY (`id`) REFERENCES `Appuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Agent`
--

LOCK TABLES `Agent` WRITE;
/*!40000 ALTER TABLE `Agent` DISABLE KEYS */;
INSERT INTO `Agent` VALUES (1,'Mikkel','Winden','2020-06-15 08:08:47.799567','shyenatech','2020-06-15 08:08:47.799614','shyenatech',3,1,'N',NULL,NULL),(2,'ffdf','tghhtr','2020-06-22 10:54:35.549473','shyenatech','2020-06-22 10:54:35.549501','shyenatech',3,3,'N',2,'rttrt'),(3,'TRy','shdg','2020-06-29 13:28:03.645630','shyenatech','2020-06-29 13:28:03.645660','shyenatech',3,3,'N',2,'2424ceh');
/*!40000 ALTER TABLE `Agent` ENABLE KEYS */;
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
