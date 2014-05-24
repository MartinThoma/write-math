-- phpMyAdmin SQL Dump
-- version 3.5.4
-- http://www.phpmyadmin.net
--
-- Host: 134.0.30.203:3306
-- Erstellungszeit: 24. Mai 2014 um 21:43
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
-- Tabellenstruktur für Tabelle `wm_invalid_formula_requests`
--

CREATE TABLE IF NOT EXISTS `wm_invalid_formula_requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_request_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `requests` int(11) NOT NULL DEFAULT '1',
  `latex` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `latex` (`latex`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=5 ;

--
-- Daten für Tabelle `wm_invalid_formula_requests`
--

INSERT INTO `wm_invalid_formula_requests` (`id`, `last_request_time`, `requests`, `latex`) VALUES
(3, '2014-05-22 11:39:59', 2, '$\\subseteq$'),
(4, '2014-05-22 11:40:03', 2, '$\\Omega$');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
