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
-- Table structure for table `Submenu`
--

DROP TABLE IF EXISTS `Submenu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Submenu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `submenu` varchar(30) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `created_by` varchar(20) NOT NULL,
  `modified_on` datetime(6) DEFAULT NULL,
  `modified_by` varchar(20) NOT NULL,
  `menu_id` int(11) NOT NULL,
  `is_deleted` varchar(1) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Submenu_menu_id_135cdf17_fk_Menu_id` (`menu_id`),
  CONSTRAINT `Submenu_menu_id_135cdf17_fk_Menu_id` FOREIGN KEY (`menu_id`) REFERENCES `Menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Submenu`
--

LOCK TABLES `Submenu` WRITE;
/*!40000 ALTER TABLE `Submenu` DISABLE KEYS */;
INSERT INTO `Submenu` VALUES (5,'User','2020-05-07 07:22:17.076049','shyenatech','2020-06-19 09:39:26.971625','shyenatech',7,'N','/Admin/User/'),(19,'Roles','2020-05-11 06:23:28.704792','shyenatech','2020-05-11 06:23:28.704830','shyenatech',7,'N','/Admin/Roles/'),(30,'Agent','2020-06-19 09:39:45.197365','shyenatech','2020-06-19 09:39:45.197444','shyenatech',7,'N','/Admin/Agent/'),(31,'Multiple People','2020-06-19 09:44:24.863406','shyenatech','2020-06-19 09:44:24.863462','shyenatech',4,'N','/Dashboard/'),(32,'Mobile Detected','2020-06-19 09:44:36.754999','shyenatech','2020-06-19 09:44:36.755039','shyenatech',4,'N','/Dashboard/'),(33,'Unidentified Person','2020-06-19 09:44:46.736486','shyenatech','2020-06-19 09:44:46.736511','shyenatech',4,'N','/Dashboard/'),(34,'Camera Tampering Count','2020-06-19 09:45:09.390451','shyenatech','2020-06-19 09:45:09.390490','shyenatech',4,'N','/Dashboard/'),(38,'Reports','2020-06-19 10:24:24.509643','shyenatech','2020-06-19 10:24:24.509671','shyenatech',6,'N','/Report/'),(40,'Current','2020-06-26 06:41:42.431120','shyenatech','2020-06-26 06:41:42.431155','shyenatech',10,'N',NULL),(41,'Old','2020-06-26 06:41:54.728141','shyenatech','2020-06-26 06:41:54.728232','shyenatech',10,'N',NULL);
/*!40000 ALTER TABLE `Submenu` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-03 16:12:18
