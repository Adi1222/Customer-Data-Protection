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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add algo_master',7,'add_algo_master'),(26,'Can change algo_master',7,'change_algo_master'),(27,'Can delete algo_master',7,'delete_algo_master'),(28,'Can view algo_master',7,'view_algo_master'),(29,'Can add menu',8,'add_menu'),(30,'Can change menu',8,'change_menu'),(31,'Can delete menu',8,'delete_menu'),(32,'Can view menu',8,'view_menu'),(33,'Can add role',9,'add_role'),(34,'Can change role',9,'change_role'),(35,'Can delete role',9,'delete_role'),(36,'Can view role',9,'view_role'),(37,'Can add submenu',10,'add_submenu'),(38,'Can change submenu',10,'change_submenu'),(39,'Can delete submenu',10,'delete_submenu'),(40,'Can view submenu',10,'view_submenu'),(41,'Can add roledetail',11,'add_roledetail'),(42,'Can change roledetail',11,'change_roledetail'),(43,'Can delete roledetail',11,'delete_roledetail'),(44,'Can view roledetail',11,'view_roledetail'),(45,'Can add camera',12,'add_camera'),(46,'Can change camera',12,'change_camera'),(47,'Can delete camera',12,'delete_camera'),(48,'Can view camera',12,'view_camera'),(49,'Can add cluster',13,'add_cluster'),(50,'Can change cluster',13,'change_cluster'),(51,'Can delete cluster',13,'delete_cluster'),(52,'Can view cluster',13,'view_cluster'),(53,'Can add bill_plan',14,'add_bill_plan'),(54,'Can change bill_plan',14,'change_bill_plan'),(55,'Can delete bill_plan',14,'delete_bill_plan'),(56,'Can view bill_plan',14,'view_bill_plan'),(57,'Can add cust_org',15,'add_cust_org'),(58,'Can change cust_org',15,'change_cust_org'),(59,'Can delete cust_org',15,'delete_cust_org'),(60,'Can view cust_org',15,'view_cust_org'),(61,'Can add agent',16,'add_agent'),(62,'Can change agent',16,'change_agent'),(63,'Can delete agent',16,'delete_agent'),(64,'Can view agent',16,'view_agent'),(65,'Can add incident',17,'add_incident'),(66,'Can change incident',17,'change_incident'),(67,'Can delete incident',17,'delete_incident'),(68,'Can view incident',17,'view_incident'),(69,'Can add appuser',18,'add_appuser'),(70,'Can change appuser',18,'change_appuser'),(71,'Can delete appuser',18,'delete_appuser'),(72,'Can view appuser',18,'view_appuser');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
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
