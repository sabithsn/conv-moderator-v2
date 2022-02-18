-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: google
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.18.04.1

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
-- Table structure for table `annotation`
--

DROP TABLE IF EXISTS `annotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `annotation` (
  `id_annotation` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_annotator` char(10) NOT NULL,
  `caption` text NOT NULL,
  `url` text NOT NULL,
  `cb0` enum('0','1') NOT NULL,
  `cb1` enum('0','1') NOT NULL,
  `cb2` enum('0','1') DEFAULT NULL,
  `cb3` enum('0','1') NOT NULL,
  `cb4` enum('0','1') NOT NULL,
  `cb5` enum('0','1') NOT NULL,
  `cb6` enum('0','1') NOT NULL,
  `other` text,
  `cbWhen` enum('0','1') NOT NULL DEFAULT '0',
  `cbHow` enum('0','1') NOT NULL DEFAULT '0',
  `cbWhere` enum('0','1') NOT NULL DEFAULT '0',
  `Identification` enum('0','1') NOT NULL DEFAULT '0',
  `source` varchar(100) DEFAULT NULL,
  `cbBrokenImg` enum('0','1') NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_annotation`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=latin1;

ALTER TABLE annotation ADD `cbMetaGood` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbMetaBad` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbVisible1` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbVisible2` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbVisible3` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbVisible4` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbVisible5` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbSubjectiveBad` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbSubjectiveGood` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbStory1` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbStory2` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbStory3` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbStory4` enum('0','1') NOT NULL DEFAULT '0';
ALTER TABLE annotation ADD `cbStory5` enum('0','1') NOT NULL DEFAULT '0';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `annotator`
--

DROP TABLE IF EXISTS `annotator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `annotator` (
  `id_annotator` char(10) NOT NULL,
  `passwd_annotator` char(6) DEFAULT NULL,
  PRIMARY KEY (`id_annotator`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

INSERT INTO annotator (id_annotator, passwd_annotator) VALUES ('mert', '0000');

INSERT INTO annotator (id_annotator, passwd_annotator) VALUES ('kat','kat');
INSERT INTO annotator (id_annotator, passwd_annotator) VALUES ('iliana','iliana');
INSERT INTO annotator (id_annotator, passwd_annotator) VALUES (1,'kappa');
INSERT INTO annotator (id_annotator, passwd_annotator) VALUES (2,'kat');
INSERT INTO annotator (id_annotator, passwd_annotator) VALUES (3,'ilana');
INSERT INTO annotator (id_annotator, passwd_annotator) VALUES (4,'mert');

SELECT * FROM annotation INTO LOCAL OUTFILE 'ilana_test_annotations.tsv'
FIELDS ENCLOSED BY '"'
TERMINATED BY ';'
ESCAPED BY '"'
LINES TERMINATED BY '\r\n';

-- Dump completed on 2020-04-13  6:51:35
