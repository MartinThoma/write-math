-- phpMyAdmin SQL Dump
-- version 4.0.6deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 07. Mai 2014 um 16:05
-- Server Version: 5.5.37-0ubuntu0.13.10.1
-- PHP-Version: 5.5.3-1ubuntu2.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `write-math`
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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=9 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_formula`
--

CREATE TABLE IF NOT EXISTS `wm_formula` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formula_name` varchar(255) COLLATE utf8_bin NOT NULL COMMENT 'Has to be displayable by HTML',
  `description` text COLLATE utf8_bin NOT NULL,
  `formula_in_latex` text COLLATE utf8_bin NOT NULL,
  `svg` text COLLATE utf8_bin NOT NULL,
  `is_single_symbol` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `formula_name` (`formula_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=197 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=117 ;

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
-- Tabellenstruktur für Tabelle `wm_openid`
--

CREATE TABLE IF NOT EXISTS `wm_openid` (
  `id` int(11) NOT NULL,
  `openid_url` varchar(255) COLLATE utf8_bin NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `openid_url_2` (`openid_url`),
  KEY `user_id` (`user_id`)
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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=140 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_raw_draw_data`
--

CREATE TABLE IF NOT EXISTS `wm_raw_draw_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `data` text COLLATE utf8_bin NOT NULL,
  `creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_agent` varchar(255) COLLATE utf8_bin NOT NULL,
  `accepted_formula_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `accepted_formula_id` (`accepted_formula_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=205 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_tag2formula`
--

CREATE TABLE IF NOT EXISTS `wm_tag2formula` (
  `tag_id` int(11) NOT NULL,
  `formula_id` int(11) NOT NULL,
  PRIMARY KEY (`tag_id`,`formula_id`),
  KEY `formula_id` (`formula_id`),
  KEY `tag_id` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_tag2user`
--

CREATE TABLE IF NOT EXISTS `wm_tag2user` (
  `user_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`tag_id`),
  KEY `tag_id` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_tags`
--

CREATE TABLE IF NOT EXISTS `wm_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `tag_description` text COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag_name` (`tag_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_users`
--

CREATE TABLE IF NOT EXISTS `wm_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `display_name` varchar(20) COLLATE utf8_bin NOT NULL,
  `email` varchar(255) COLLATE utf8_bin NOT NULL,
  `password` char(32) COLLATE utf8_bin NOT NULL,
  `salt` varchar(255) COLLATE utf8_bin NOT NULL,
  `language` char(2) COLLATE utf8_bin DEFAULT NULL,
  `handedness` char(1) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `display_name` (`display_name`),
  UNIQUE KEY `email` (`email`),
  KEY `language` (`language`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=12 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=18 ;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `wm_formula2challenge`
--
ALTER TABLE `wm_formula2challenge`
  ADD CONSTRAINT `wm_formula2challenge_ibfk_1` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wm_formula2challenge_ibfk_2` FOREIGN KEY (`challenge_id`) REFERENCES `wm_challenges` (`id`) ON DELETE CASCADE;

--
-- Constraints der Tabelle `wm_openid`
--
ALTER TABLE `wm_openid`
  ADD CONSTRAINT `wm_openid_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`);

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
-- Constraints der Tabelle `wm_tag2formula`
--
ALTER TABLE `wm_tag2formula`
  ADD CONSTRAINT `wm_tag2formula_ibfk_1` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`),
  ADD CONSTRAINT `wm_tag2formula_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `wm_tags` (`id`);

--
-- Constraints der Tabelle `wm_tag2user`
--
ALTER TABLE `wm_tag2user`
  ADD CONSTRAINT `wm_tag2user_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`),
  ADD CONSTRAINT `wm_tag2user_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `wm_tags` (`id`);

--
-- Constraints der Tabelle `wm_users`
--
ALTER TABLE `wm_users`
  ADD CONSTRAINT `wm_users_ibfk_1` FOREIGN KEY (`language`) REFERENCES `wm_languages` (`language_code`);

--
-- Constraints der Tabelle `wm_votes`
--
ALTER TABLE `wm_votes`
  ADD CONSTRAINT `uservote_rawdata2formula_id` FOREIGN KEY (`raw_data2formula_id`) REFERENCES `wm_raw_data2formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `uservote_userid` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
