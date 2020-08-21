CREATE TABLE `sample_table` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `uuid` char(36) NOT NULL,
    `my_name` varchar(255) DEFAULT '',
    `is_true` tinyint(1) DEFAULT 0,
    `created_at` datetime,
    `another_int` int(11) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;
