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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-06-12 11:27:43.156083'),(2,'auth','0001_initial','2020-06-12 11:27:43.769252'),(3,'admin','0001_initial','2020-06-12 11:27:45.203050'),(4,'admin','0002_logentry_remove_auto_add','2020-06-12 11:27:45.548584'),(5,'admin','0003_logentry_add_action_flag_choices','2020-06-12 11:27:45.566214'),(6,'admin','0004_auto_20200513_0730','2020-06-12 11:27:45.768872'),(7,'admin','0005_auto_20200513_0832','2020-06-12 11:27:45.988934'),(8,'admin','0006_auto_20200513_0835','2020-06-12 11:27:46.198998'),(9,'admin','0007_auto_20200513_0835','2020-06-12 11:27:46.398618'),(10,'admin','0008_auto_20200513_0838','2020-06-12 11:27:46.608480'),(11,'contenttypes','0002_remove_content_type_name','2020-06-12 11:27:46.857613'),(12,'auth','0002_alter_permission_name_max_length','2020-06-12 11:27:47.076751'),(13,'auth','0003_alter_user_email_max_length','2020-06-12 11:27:47.138135'),(14,'auth','0004_alter_user_username_opts','2020-06-12 11:27:47.160170'),(15,'auth','0005_alter_user_last_login_null','2020-06-12 11:27:47.289063'),(16,'auth','0006_require_contenttypes_0002','2020-06-12 11:27:47.297004'),(17,'auth','0007_alter_validators_add_error_messages','2020-06-12 11:27:47.312175'),(18,'auth','0008_alter_user_username_max_length','2020-06-12 11:27:47.346591'),(19,'auth','0009_alter_user_last_name_max_length','2020-06-12 11:27:47.377481'),(20,'auth','0010_alter_group_name_max_length','2020-06-12 11:27:47.409641'),(21,'auth','0011_update_proxy_permissions','2020-06-12 11:27:47.429522'),(22,'sessions','0001_initial','2020-06-12 11:27:47.510544'),(23,'cdpapp','0001_initial','2020-06-12 11:28:37.783634'),(24,'cdpapp','0002_auto_20200612_1129','2020-06-12 11:29:17.883026'),(25,'cdpapp','0003_auto_20200612_1131','2020-06-12 11:31:33.971957');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
