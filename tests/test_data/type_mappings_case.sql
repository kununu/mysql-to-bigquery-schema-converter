/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `type_mappings_case` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `views` mediumint(8) unsigned NOT NULL,
  `cluster` bigint(20) DEFAULT NULL,
  `uuid` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '(DC2Type:uuid)',
  `title` varchar(90) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_primary` tinyint(1),
  `flag` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `locale` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `publication_date` date NOT NULL,
  `status` enum('online','offline','default') NOT NULL DEFAULT 'default',
  `benefits` set('1','2','3') NOT NULL DEFAULT '',
  `answer` text COLLATE utf8_unicode_ci,
  `lat` float(9,6) NOT NULL,
  `weight` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_91416C22D17F50A6` (`uuid`),
  KEY `IDX_91416C2245B63C23` (`views`,`locale`,`is_primary`,`flag`),
  CONSTRAINT `FK_91416C2245B63C23` FOREIGN KEY (`views`) REFERENCES `views` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44834 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
