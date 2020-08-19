/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_titles` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `job_title_group_id` int(10) unsigned NOT NULL,
  `uuid` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '(DC2Type:uuid)',
  `title` varchar(90) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `flag` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `locale` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_91416C22D17F50A6` (`uuid`),
  KEY `IDX_91416C2245B63C23` (`job_title_group_id`,`locale`,`is_primary`,`flag`),
  CONSTRAINT `FK_91416C2245B63C23` FOREIGN KEY (`job_title_group_id`) REFERENCES `job_title_groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44834 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
