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
-- Table structure for table `Appuser`
--

DROP TABLE IF EXISTS `Appuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Appuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_deleted` varchar(1) NOT NULL,
  `mobile` varchar(12) DEFAULT NULL,
  `is_superuser` varchar(1) NOT NULL,
  `designation` varchar(20) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `created_by` varchar(20) NOT NULL,
  `modified_on` datetime(6) DEFAULT NULL,
  `modified_by` varchar(20) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `profile_pic` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `Appuser_customer_id_69096f53_fk_Cust_org_id` (`customer_id`),
  KEY `Appuser_role_id_0658db09_fk_Role_id` (`role_id`),
  CONSTRAINT `Appuser_customer_id_69096f53_fk_Cust_org_id` FOREIGN KEY (`customer_id`) REFERENCES `Cust_org` (`id`),
  CONSTRAINT `Appuser_role_id_0658db09_fk_Role_id` FOREIGN KEY (`role_id`) REFERENCES `Role` (`id`),
  CONSTRAINT `Appuser_user_id_f7e4374e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Appuser`
--

LOCK TABLES `Appuser` WRITE;
/*!40000 ALTER TABLE `Appuser` DISABLE KEYS */;
INSERT INTO `Appuser` VALUES (1,'N',NULL,'Y','Lead','2020-05-13 16:06:57.000000','Shyena Tech','2020-05-13 16:06:57.000000','Shyena Tech',3,27,4,'sty.jpeg'),(2,'N','9898789878','N','Manager','2020-05-13 12:10:33.069515','Shyena Tech','2020-05-13 12:10:33.069549','Shyena Tech',2,36,5,'Aron.jpg'),(3,'N','','N','Lead','2020-05-13 12:26:48.253883','AronFinch@1','2020-05-13 12:26:48.253911','AronFinch@1',2,35,7,'Rahul.jpg'),(4,'N','9897675671','N','Manager','2020-05-13 12:37:01.976229','Shyena Tech','2020-05-13 12:37:01.976229','Shyena Tech',1,36,8,'virat.jpg'),(5,'N','9989342167','N','Lead','2020-05-13 12:54:09.615674','Virat@1','2020-05-13 12:54:09.615674','Virat@1',1,35,9,'Ayush.jpg'),(6,'N','9123456321','N','Lead','2020-06-19 08:15:09.790286','Shyena Tech','2020-06-19 08:15:09.790369','Shyena Tech',1,34,10,''),(7,'N','897866789','N','Manager','2020-06-19 08:36:14.992697','AronFinch@1','2020-06-19 08:36:14.992738','AronFinch@1',2,33,11,'');
/*!40000 ALTER TABLE `Appuser` ENABLE KEYS */;
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
