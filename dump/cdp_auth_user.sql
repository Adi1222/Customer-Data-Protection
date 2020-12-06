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
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (4,'pbkdf2_sha256$150000$3z6CHqnNb9RF$xBvuTvk7WctpCN2QEcL2aY6nFXc6+M7HBcimeVAiYtk=','2020-07-01 07:10:20.274656',1,'shyenatech','Shyena','Tech','sty@example.com',1,1,'2020-05-13 09:36:02.807186'),(5,'pbkdf2_sha256$150000$3VqA7FzgRFdh$CR6q4SMwZS9LwLtwaIRmL8hqBGlC6AES2lUWyDsPYY8=','2020-06-26 10:15:51.811900',0,'AronFinch@1','Aron','Finch','af@gmail.com',0,1,'2020-05-13 12:10:32.902278'),(7,'pbkdf2_sha256$150000$yQKpel0IqrsQ$yqbHa7PhJ+UkQGw22G8PGQAFh/whFkVZGTe0EiW5j2c=','2020-05-22 07:53:50.809728',0,'RahulS1','Rahul','Sharma','rahul@gmail.com',0,1,'2020-05-13 12:26:47.391071'),(8,'pbkdf2_sha256$150000$cLTxHT26mUeV$HMxUcR9nk4DPIblGu/mby1IiP2g7Bh2J46i3fkuRgOo=','2020-06-29 13:46:00.169313',0,'Virat@1','Virat','Kohli','vk@gmail.com',0,1,'2020-05-13 12:37:01.827426'),(9,'pbkdf2_sha256$150000$7fgo56Q521Kt$F0pdr4K63MR41QW8xHy2rojfoY6ve6x+qMxMqAcV6vI=','2020-06-29 13:45:36.690515',0,'Ayush@1','Ayush','Verma','av@gmail.com',0,1,'2020-05-13 12:54:09.443122'),(10,'pbkdf2_sha256$150000$3z6CHqnNb9RF$xBvuTvk7WctpCN2QEcL2aY6nFXc6+M7HBcimeVAiYtk=','2020-06-19 10:04:58.475419',0,'Ani@1','','','ani77@try.com',0,1,'2020-06-19 08:15:08.298948'),(11,'pbkdf2_sha256$150000$lfP8DtsCDx4k$RsmuItSq3zH0jAkeUxCQA7qlbzBz6jogdqkReeNJ9Kc=','2020-06-19 08:36:44.262606',0,'YashR@1','','','yash77@try.com',0,1,'2020-06-19 08:36:14.859668');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
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
