-- phpMyAdmin SQL Dump
-- version 3.5.4
-- http://www.phpmyadmin.net
--
-- Host: 134.0.30.203:3306
-- Erstellungszeit: 24. Mai 2014 um 21:44
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

--
-- Daten für Tabelle `wm_similarity`
--

INSERT INTO `wm_similarity` (`id`, `base_symbol`, `similar_symbol`, `comment_choice`) VALUES
(2, 72, 989, '2 is the standard way to write 2 - all other stuff is done with math mode'),
(3, 73, 983, '3 is the standard way to write 3 - all other stuff is done with math mode'),
(5, 49, 1011, 'S and \\mathcal{S}'),
(6, 33, 995, 'C and \\mathcal{C}'),
(7, 37, 300, ''),
(8, 160, 862, 'up[greekletter] is so useless...'),
(9, 42, 315, ''),
(10, 537, 978, 'completely round circle - only the scaling varies'),
(11, 537, 502, 'completely round circle - width differs'),
(12, 537, 518, 'completely round circle - size differs'),
(13, 537, 565, ''),
(14, 513, 986, ''),
(15, 187, 925, ''),
(16, 187, 353, ''),
(17, 180, 374, ''),
(18, 82, 848, ''),
(19, 87, 310, 'text[greekletter] is useless'),
(20, 169, 872, 'up[greekletter]'),
(21, 171, 876, 'up[greekletter]'),
(22, 168, 869, 'up[greekletter]');

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `wm_similarity`
--
ALTER TABLE `wm_similarity`
  ADD CONSTRAINT `wm_similarity_ibfk_2` FOREIGN KEY (`similar_symbol`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_similarity_ibfk_1` FOREIGN KEY (`base_symbol`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
