--
-- Datenbank: `20080912003-1`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_flags`
--

CREATE TABLE IF NOT EXISTS `wm_flags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `raw_data_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_flags` (`user_id`,`raw_data_id`),
  KEY `user_id` (`user_id`),
  KEY `raw_data_id` (`raw_data_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_formula`
--

CREATE TABLE IF NOT EXISTS `wm_formula` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '10',
  `formula_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `description` text COLLATE utf8_bin NOT NULL,
  `formula_in_latex` text COLLATE utf8_bin NOT NULL,
  `unicode_dec` int(11) NOT NULL,
  `font` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT 'STIXGeneral',
  `font_style` enum('normal','italic') COLLATE utf8_bin NOT NULL DEFAULT 'normal',
  `unicodexml_description` varchar(255) COLLATE utf8_bin NOT NULL,
  `mode` enum('bothmodes','textmode','mathmode') COLLATE utf8_bin NOT NULL DEFAULT 'bothmodes',
  `preamble` text COLLATE utf8_bin NOT NULL,
  `best_rendering` int(11) DEFAULT NULL,
  `formula_type` enum('single symbol','formula','drawing','nesting symbol') COLLATE utf8_bin DEFAULT NULL,
  `variant_of` int(11) DEFAULT NULL,
  `for_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'last edit',
  PRIMARY KEY (`id`),
  UNIQUE KEY `formula_name` (`formula_name`),
  KEY `best_rendering` (`best_rendering`),
  KEY `user_id` (`user_id`),
  KEY `variant_of` (`variant_of`)
) ENGINE=InnoDB AUTO_INCREMENT=4943 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_formula_in_paper`
--

CREATE TABLE IF NOT EXISTS `wm_formula_in_paper` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol_id` int(11) NOT NULL,
  `paper` varchar(255) COLLATE utf8_bin NOT NULL,
  `meaning` varchar(255) COLLATE utf8_bin NOT NULL,
  `inserted_by` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `symbol_id_2` (`symbol_id`,`paper`),
  KEY `symbol_id` (`symbol_id`),
  KEY `paper_id` (`paper`),
  KEY `inserted_by` (`inserted_by`)
) ENGINE=InnoDB AUTO_INCREMENT=228 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_formula_old`
--

CREATE TABLE IF NOT EXISTS `wm_formula_old` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formula_id` int(11) NOT NULL,
  `description` text COLLATE utf8_bin NOT NULL,
  `user_id` int(11) NOT NULL COMMENT 'editor',
  `for_timestamp` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `formula_id` (`formula_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1025 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='This is not an outdated table, but version control';

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_formula_svg_missing`
--

CREATE TABLE IF NOT EXISTS `wm_formula_svg_missing` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `formula_id` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `useragent` varchar(255) CHARACTER SET latin1 NOT NULL,
  `problem_type` enum('svg missing','rendering wrong') COLLATE utf8_bin NOT NULL DEFAULT 'svg missing',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_2` (`user_id`,`formula_id`),
  KEY `user_id` (`user_id`,`formula_id`),
  KEY `formula_id` (`formula_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18868 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_invalid_formula_requests`
--

CREATE TABLE IF NOT EXISTS `wm_invalid_formula_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_request_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `requests` int(11) NOT NULL DEFAULT '1',
  `latex` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `latex` (`latex`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_languages`
--

CREATE TABLE IF NOT EXISTS `wm_languages` (
  `language_code` char(2) COLLATE utf8_bin NOT NULL,
  `english_language_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `native_language_name` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`language_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_papers`
--

CREATE TABLE IF NOT EXISTS `wm_papers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `arxiv_identifier` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `arxiv_tar_file` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `arxiv_folder_in_tar_file` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_partial_answer`
--

CREATE TABLE IF NOT EXISTS `wm_partial_answer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `recording_id` int(11) NOT NULL,
  `strokes` varchar(255) COLLATE utf8_bin NOT NULL,
  `symbol_id` int(11) NOT NULL,
  `is_accepted` tinyint(1) NOT NULL DEFAULT '0',
  `probability` double unsigned NOT NULL DEFAULT '1',
  `creation_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_worker_answer` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `recording_id_2` (`recording_id`,`symbol_id`,`strokes`),
  KEY `user_id` (`user_id`,`recording_id`,`symbol_id`),
  KEY `recording_id` (`recording_id`),
  KEY `symbol_id` (`symbol_id`)
) ENGINE=InnoDB AUTO_INCREMENT=49371 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_raw_draw_data`
--

CREATE TABLE IF NOT EXISTS `wm_raw_draw_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `secret` char(36) COLLATE utf8_bin NOT NULL DEFAULT '',
  `data` mediumtext COLLATE utf8_bin NOT NULL,
  `description` text COLLATE utf8_bin NOT NULL,
  `internal_id` varchar(255) COLLATE utf8_bin NOT NULL,
  `nr_of_symbols` int(11) NOT NULL DEFAULT '1',
  `segmentation` text COLLATE utf8_bin,
  `stroke_segmentable` tinyint(1) NOT NULL DEFAULT '1',
  `classifiable` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'some drawings cannot be distinguished',
  `no_geometry` tinyint(1) NOT NULL DEFAULT '0',
  `md5data` char(32) COLLATE utf8_bin NOT NULL DEFAULT '',
  `creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ip` varbinary(16) DEFAULT NULL,
  `user_agent` varchar(255) COLLATE utf8_bin NOT NULL,
  `device_type` enum('unknown','mouse','touch','stylus') COLLATE utf8_bin NOT NULL DEFAULT 'unknown',
  `accepted_formula_id` int(11) DEFAULT NULL,
  `wild_point_count` smallint(6) NOT NULL DEFAULT '0',
  `missing_line` tinyint(1) NOT NULL DEFAULT '0',
  `has_hook` tinyint(1) NOT NULL DEFAULT '0',
  `has_too_long_line` tinyint(1) NOT NULL DEFAULT '0',
  `has_interrupted_line` tinyint(1) NOT NULL DEFAULT '0',
  `has_correction` tinyint(1) NOT NULL DEFAULT '0',
  `is_image` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'is an image, not a formula',
  `other_problem` tinyint(1) NOT NULL DEFAULT '0',
  `administrator_edit` timestamp NULL DEFAULT NULL,
  `is_in_testset` tinyint(1) NOT NULL DEFAULT '0',
  `inkml` text COLLATE utf8_bin NOT NULL,
  `user_answers_count` smallint(5) unsigned NOT NULL DEFAULT '0',
  `automated_answers_count` smallint(5) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_2` (`user_id`,`md5data`),
  KEY `user_id` (`user_id`),
  KEY `accepted_formula_id` (`accepted_formula_id`)
) ENGINE=InnoDB AUTO_INCREMENT=330235 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_renderings`
--

CREATE TABLE IF NOT EXISTS `wm_renderings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formula_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `creation_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `svg` text COLLATE utf8_bin NOT NULL,
  `png_16` blob COMMENT 'with of 16 px',
  PRIMARY KEY (`id`),
  KEY `formula_id` (`formula_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2237 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_similarity`
--

CREATE TABLE IF NOT EXISTS `wm_similarity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `base_symbol` int(11) NOT NULL,
  `similar_symbol` int(11) NOT NULL,
  `comment_choice` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  KEY `base_symbol` (`base_symbol`),
  KEY `simmilar_symbol` (`similar_symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_tags`
--

CREATE TABLE IF NOT EXISTS `wm_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `is_package` tinyint(1) NOT NULL DEFAULT '0',
  `description` text COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag_name` (`tag_name`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_tags2symbols`
--

CREATE TABLE IF NOT EXISTS `wm_tags2symbols` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_id` int(11) NOT NULL,
  `symbol_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `max_one_tag_per_symb` (`tag_id`,`symbol_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9517 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_user_unknown_formula`
--

CREATE TABLE IF NOT EXISTS `wm_user_unknown_formula` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `formula_id` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`formula_id`),
  KEY `user_id_2` (`user_id`),
  KEY `formula_id` (`formula_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10214 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_users`
--

CREATE TABLE IF NOT EXISTS `wm_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `display_name` varchar(30) COLLATE utf8_bin NOT NULL,
  `email` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `password` char(60) COLLATE utf8_bin NOT NULL,
  `account_type` enum('IP-User','Regular User','Admin','Worker') COLLATE utf8_bin NOT NULL DEFAULT 'Regular User',
  `confirmation_code` char(32) COLLATE utf8_bin NOT NULL,
  `status` enum('activated','deactivated') COLLATE utf8_bin NOT NULL,
  `language` char(2) COLLATE utf8_bin DEFAULT NULL,
  `handedness` enum('l','r') COLLATE utf8_bin DEFAULT NULL,
  `description` text COLLATE utf8_bin NOT NULL,
  `latest_heartbeat` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `display_name` (`display_name`),
  UNIQUE KEY `email` (`email`),
  KEY `language` (`language`)
) ENGINE=InnoDB AUTO_INCREMENT=608525 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_users_backup`
--

CREATE ALGORITHM=UNDEFINED DEFINER=`20080912003-1`@`%` SQL SECURITY DEFINER VIEW `wm_users_backup` AS select `wm_users`.`id` AS `id`,`wm_users`.`display_name` AS `display_name`,`wm_users`.`account_type` AS `account_type`,`wm_users`.`status` AS `status`,`wm_users`.`language` AS `language`,`wm_users`.`handedness` AS `handedness`,`wm_users`.`description` AS `description` from `wm_users`;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_workers`
--

CREATE TABLE IF NOT EXISTS `wm_workers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `has_user_id` int(11) NOT NULL,
  `API_key` varchar(32) COLLATE utf8_bin NOT NULL,
  `display_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `description` text COLLATE utf8_bin NOT NULL,
  `url` varchar(255) COLLATE utf8_bin NOT NULL,
  `latest_heartbeat` timestamp NULL DEFAULT NULL,
  `status` enum('active','deactivated') COLLATE utf8_bin NOT NULL DEFAULT 'active',
  PRIMARY KEY (`id`),
  UNIQUE KEY `worker_name` (`display_name`),
  UNIQUE KEY `API_key` (`API_key`),
  UNIQUE KEY `url` (`url`),
  KEY `user_id` (`user_id`),
  KEY `has_user_id` (`has_user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

