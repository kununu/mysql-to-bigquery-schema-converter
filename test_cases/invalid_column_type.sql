CREATE TABLE `simple_table` (
    `id` my_special_type(420) unsigned NOT NULL AUTO_INCREMENT,
    `uuid` char(36) NOT NULL,
    `my_name` varchar(255) DEFAULT '',
    `is_true` tinyint(1) DEFAULT 0,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;
