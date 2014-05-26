DROP TABLE IF EXISTS `temperature`;

CREATE TABLE `temperature` (
  `timestamp` datetime NOT NULL DEFAULT 0,
  `id` int(11) NOT NULL DEFAULT '0',
  `value` double DEFAULT NULL,
  PRIMARY KEY (`timestamp`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
