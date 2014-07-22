-- phpMyAdmin SQL Dump
-- version 3.5.4
-- http://www.phpmyadmin.net
--
-- Host: 134.0.30.203:3306
-- Erstellungszeit: 22. Jul 2014 um 02:26
-- Server Version: 5.5.28a-MariaDB
-- PHP-Version: 5.3.19

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Datenbank: `20080912003-1`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_challenges`
--

CREATE TABLE IF NOT EXISTS `wm_challenges` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge_name` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `challenge_name` (`challenge_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=10 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_dtw_worker_data`
--

CREATE TABLE IF NOT EXISTS `wm_dtw_worker_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data` text COLLATE utf8_bin NOT NULL,
  `preprocessed_data` text COLLATE utf8_bin NOT NULL,
  `nr_of_symbols` int(11) NOT NULL,
  `accepted_formula_id` int(11) DEFAULT NULL,
  `nr_of_lines` tinyint(4) NOT NULL,
  `nr_of_points` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=2 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=39 ;

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
  `mode` enum('bothmodes','textmode','mathmode') COLLATE utf8_bin NOT NULL DEFAULT 'bothmodes',
  `package` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `preamble` text COLLATE utf8_bin NOT NULL,
  `best_rendering` int(11) DEFAULT NULL,
  `formula_type` enum('single symbol','formula','drawing','nesting symbol') COLLATE utf8_bin DEFAULT NULL,
  `is_important` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `best_rendering` (`best_rendering`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1513 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_formula2challenge`
--

CREATE TABLE IF NOT EXISTS `wm_formula2challenge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge_id` int(11) NOT NULL,
  `formula_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `formula_id` (`formula_id`,`challenge_id`),
  KEY `challenge_id` (`challenge_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=134 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_formula_in_paper`
--

CREATE TABLE IF NOT EXISTS `wm_formula_in_paper` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol_id` int(11) NOT NULL,
  `paper_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `symbol_id` (`symbol_id`),
  KEY `paper_id` (`paper_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

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
  UNIQUE KEY `user_id_2_formula_svg_missing` (`user_id`,`formula_id`),
  KEY `user_id` (`user_id`,`formula_id`),
  KEY `formula_id` (`formula_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=379 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=6 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_raw_data2formula`
--

CREATE TABLE IF NOT EXISTS `wm_raw_data2formula` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `raw_data_id` int(11) NOT NULL,
  `formula_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `raw_data_id_2` (`raw_data_id`,`formula_id`),
  KEY `raw_data_id` (`raw_data_id`,`formula_id`,`user_id`),
  KEY `formula_id` (`formula_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=19718 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_raw_draw_data`
--

CREATE TABLE IF NOT EXISTS `wm_raw_draw_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `data` text COLLATE utf8_bin NOT NULL,
  `nr_of_symbols` int(11) NOT NULL DEFAULT '1',
  `md5data` char(32) COLLATE utf8_bin NOT NULL DEFAULT '',
  `creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_agent` varchar(255) COLLATE utf8_bin NOT NULL,
  `accepted_formula_id` int(11) DEFAULT NULL,
  `wild_point_count` smallint(6) NOT NULL DEFAULT '0',
  `missing_line` tinyint(1) NOT NULL DEFAULT '0',
  `has_hook` tinyint(1) NOT NULL DEFAULT '0',
  `has_too_long_line` tinyint(1) NOT NULL DEFAULT '0',
  `has_interrupted_line` tinyint(1) NOT NULL DEFAULT '0',
  `is_image` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'is an image, not a formula',
  `other_problem` tinyint(1) NOT NULL DEFAULT '0',
  `administrator_edit` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_2` (`user_id`,`md5data`),
  KEY `user_id` (`user_id`),
  KEY `accepted_formula_id` (`accepted_formula_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=292243 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1188 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=25 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_users`
--

CREATE TABLE IF NOT EXISTS `wm_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `display_name` varchar(20) COLLATE utf8_bin NOT NULL,
  `email` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `password` char(60) COLLATE utf8_bin NOT NULL,
  `account_type` enum('IP-User','Regular User','Admin') COLLATE utf8_bin NOT NULL DEFAULT 'Regular User',
  `confirmation_code` char(32) COLLATE utf8_bin NOT NULL,
  `status` enum('activated','deactivated') COLLATE utf8_bin NOT NULL,
  `language` char(2) COLLATE utf8_bin DEFAULT NULL,
  `handedness` enum('l','r') COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `display_name` (`display_name`),
  UNIQUE KEY `email` (`email`),
  KEY `language` (`language`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=19945 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=944 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_votes`
--

CREATE TABLE IF NOT EXISTS `wm_votes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `raw_data2formula_id` int(11) NOT NULL,
  `vote` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uservote` (`user_id`,`raw_data2formula_id`),
  KEY `raw_data2formula_id` (`raw_data2formula_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=5296 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_workers`
--

CREATE TABLE IF NOT EXISTS `wm_workers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `API_key` varchar(32) COLLATE utf8_bin NOT NULL,
  `worker_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `description` text COLLATE utf8_bin NOT NULL,
  `url` varchar(255) COLLATE utf8_bin NOT NULL,
  `latest_heartbeat` timestamp NULL DEFAULT NULL,
  `status` enum('active','deactivated') COLLATE utf8_bin NOT NULL DEFAULT 'active',
  PRIMARY KEY (`id`),
  UNIQUE KEY `worker_name` (`worker_name`),
  UNIQUE KEY `API_key` (`API_key`),
  UNIQUE KEY `url` (`url`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_worker_answers`
--

CREATE TABLE IF NOT EXISTS `wm_worker_answers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `worker_id` int(11) NOT NULL,
  `raw_data_id` int(11) NOT NULL,
  `formula_id` int(11) NOT NULL,
  `probability` double unsigned NOT NULL,
  `answer_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `formula_id` (`formula_id`),
  KEY `raw_data_id` (`raw_data_id`),
  KEY `worker_id` (`worker_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=7741 ;

