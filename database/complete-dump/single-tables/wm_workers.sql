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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=6 ;

--
-- Daten für Tabelle `wm_workers`
--

INSERT INTO `wm_workers` (`id`, `user_id`, `API_key`, `worker_name`, `description`, `url`, `latest_heartbeat`, `status`) VALUES
(4, 10, '5373c82a78230', 'DTW', 0x5468697320636c69656e74206170706c69657320612044545720746563686e697175652e, 'http://www.martin-thoma.de/write-math/clients/dtw-php/', '2014-05-15 10:12:22', 'deactivated');

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `wm_workers`
--
ALTER TABLE `wm_workers`
  ADD CONSTRAINT `wm_workers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
