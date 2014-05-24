-- phpMyAdmin SQL Dump
-- version 3.5.4
-- http://www.phpmyadmin.net
--
-- Host: 134.0.30.203:3306
-- Erstellungszeit: 24. Mai 2014 um 21:45
-- Server Version: 5.5.28a-MariaDB
-- PHP-Version: 5.3.19

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `20080912003-1`
--

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=28 ;

--
-- Daten für Tabelle `wm_votes`
--

INSERT INTO `wm_votes` (`id`, `user_id`, `raw_data2formula_id`, `vote`) VALUES
(18, 10, 215, 1),
(20, 15, 296, 1),
(22, 10, 300, 1),
(24, 10, 269, 1),
(25, 10, 731, 1),
(26, 10, 3134, 1),
(27, 46, 3134, 1);

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `wm_votes`
--
ALTER TABLE `wm_votes`
  ADD CONSTRAINT `uservote_rawdata2formula_id` FOREIGN KEY (`raw_data2formula_id`) REFERENCES `wm_raw_data2formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `uservote_userid` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
