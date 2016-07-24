CREATE TABLE `hook` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `project` int(10) unsigned NOT NULL,
  `package` int(10) unsigned NOT NULL,
  `branch` varchar(255) NOT NULL,
  `repo` int(10) unsigned NOT NULL,
  `enabled` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `table_index` (`project`,`package`,`branch`,`repo`),
  KEY `branch` (`branch`),
  KEY `package` (`package`),
  KEY `repo` (`repo`),
  CONSTRAINT `hook_ibfk_1` FOREIGN KEY (`project`) REFERENCES `project` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `hook_ibfk_2` FOREIGN KEY (`package`) REFERENCES `package` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `hook_ibfk_3` FOREIGN KEY (`repo`) REFERENCES `repo` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `hook_data` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hook` int(10) unsigned NOT NULL,
  `sha1` varchar(255) NOT NULL,
  `tag` varchar(255) NOT NULL,
  `timestamp` int(11) unsigned NOT NULL,
  UNIQUE KEY `hook` (`hook`),
  KEY `id` (`id`),
  KEY `time` (`timestamp`),
  CONSTRAINT `hook_data_ibfk_1` FOREIGN KEY (`hook`) REFERENCES `hook` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `package` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `project` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `repo` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
