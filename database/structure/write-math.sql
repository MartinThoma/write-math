-- phpMyAdmin SQL Dump
-- version 3.5.4
-- http://www.phpmyadmin.net
--
-- Host: 134.0.30.203:3306
-- Erstellungszeit: 21. Jun 2014 um 19:51
-- Server Version: 5.5.28a-MariaDB
-- PHP-Version: 5.3.19

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Datenbank: `20080912003-1`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_blacklist`
--

CREATE TABLE IF NOT EXISTS `wm_blacklist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `latex` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `latex` (`latex`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=2 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=9 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_formula`
--

CREATE TABLE IF NOT EXISTS `wm_formula` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formula_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `description` text COLLATE utf8_bin NOT NULL,
  `formula_in_latex` text COLLATE utf8_bin NOT NULL,
  `mode` enum('bothmodes','textmode','mathmode') COLLATE utf8_bin NOT NULL DEFAULT 'bothmodes',
  `package` varchar(255) COLLATE utf8_bin DEFAULT NULL,
  `preamble` text COLLATE utf8_bin NOT NULL,
  `best_rendering` int(11) DEFAULT NULL,
  `formula_type` enum('single symbol','formula','drawing','nesting symbol') COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `best_rendering` (`best_rendering`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1325 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=267 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=8063 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_raw_draw_data`
--

CREATE TABLE IF NOT EXISTS `wm_raw_draw_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `data` text COLLATE utf8_bin NOT NULL,
  `md5data` char(32) COLLATE utf8_bin NOT NULL DEFAULT '',
  `creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_agent` varchar(255) COLLATE utf8_bin NOT NULL,
  `accepted_formula_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_2` (`user_id`,`md5data`),
  KEY `user_id` (`user_id`),
  KEY `accepted_formula_id` (`accepted_formula_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=8504 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1127 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=23 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_users`
--

CREATE TABLE IF NOT EXISTS `wm_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `display_name` varchar(20) COLLATE utf8_bin NOT NULL,
  `email` varchar(255) COLLATE utf8_bin NOT NULL,
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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=92 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=826 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=29 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=4396 ;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `wm_flags`
--
ALTER TABLE `wm_flags`
  ADD CONSTRAINT `wm_flags_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_flags_ibfk_2` FOREIGN KEY (`raw_data_id`) REFERENCES `wm_raw_draw_data` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_formula`
--
ALTER TABLE `wm_formula`
  ADD CONSTRAINT `wm_formula_ibfk_1` FOREIGN KEY (`best_rendering`) REFERENCES `wm_renderings` (`id`) ON DELETE SET NULL ON UPDATE SET NULL;

--
-- Constraints der Tabelle `wm_formula2challenge`
--
ALTER TABLE `wm_formula2challenge`
  ADD CONSTRAINT `wm_formula2challenge_ibfk_1` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wm_formula2challenge_ibfk_2` FOREIGN KEY (`challenge_id`) REFERENCES `wm_challenges` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `wm_formula_svg_missing`
--
ALTER TABLE `wm_formula_svg_missing`
  ADD CONSTRAINT `wm_formula_svg_missing_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_formula_svg_missing_ibfk_2` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_raw_data2formula`
--
ALTER TABLE `wm_raw_data2formula`
  ADD CONSTRAINT `wm_raw_data2formula_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wm_raw_data2formula_ibfk_1` FOREIGN KEY (`raw_data_id`) REFERENCES `wm_raw_draw_data` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wm_raw_data2formula_ibfk_2` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `wm_raw_draw_data`
--
ALTER TABLE `wm_raw_draw_data`
  ADD CONSTRAINT `wm_raw_draw_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wm_raw_draw_data_ibfk_2` FOREIGN KEY (`accepted_formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `wm_renderings`
--
ALTER TABLE `wm_renderings`
  ADD CONSTRAINT `wm_renderings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_renderings_ibfk_1` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_similarity`
--
ALTER TABLE `wm_similarity`
  ADD CONSTRAINT `wm_similarity_ibfk_2` FOREIGN KEY (`similar_symbol`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_similarity_ibfk_1` FOREIGN KEY (`base_symbol`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_users`
--
ALTER TABLE `wm_users`
  ADD CONSTRAINT `wm_users_ibfk_1` FOREIGN KEY (`language`) REFERENCES `wm_languages` (`language_code`);

--
-- Constraints der Tabelle `wm_user_unknown_formula`
--
ALTER TABLE `wm_user_unknown_formula`
  ADD CONSTRAINT `wm_user_unknown_formula_ibfk_2` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_user_unknown_formula_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_votes`
--
ALTER TABLE `wm_votes`
  ADD CONSTRAINT `uservote_rawdata2formula_id` FOREIGN KEY (`raw_data2formula_id`) REFERENCES `wm_raw_data2formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `uservote_userid` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_workers`
--
ALTER TABLE `wm_workers`
  ADD CONSTRAINT `wm_workers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `wm_worker_answers`
--
ALTER TABLE `wm_worker_answers`
  ADD CONSTRAINT `wm_worker_answers_ibfk_1` FOREIGN KEY (`worker_id`) REFERENCES `wm_workers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_worker_answers_ibfk_2` FOREIGN KEY (`raw_data_id`) REFERENCES `wm_raw_draw_data` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_worker_answers_ibfk_3` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
