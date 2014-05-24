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

--
-- Daten für Tabelle `wm_formula2challenge`
--

INSERT INTO `wm_formula2challenge` (`id`, `challenge_id`, `formula_id`) VALUES
(1, 1, 31),
(2, 1, 32),
(3, 1, 33),
(4, 1, 34),
(5, 1, 35),
(6, 1, 36),
(7, 1, 37),
(8, 1, 38),
(9, 1, 39),
(10, 1, 40),
(11, 1, 41),
(12, 1, 42),
(13, 1, 43),
(14, 1, 44),
(15, 1, 45),
(16, 1, 46),
(26, 1, 47),
(17, 1, 48),
(18, 1, 49),
(19, 1, 50),
(20, 1, 51),
(21, 1, 52),
(22, 1, 53),
(23, 1, 54),
(24, 1, 55),
(25, 1, 56),
(27, 5, 70),
(133, 9, 70),
(28, 5, 71),
(128, 9, 71),
(29, 5, 72),
(129, 9, 72),
(30, 5, 73),
(31, 5, 74),
(32, 5, 75),
(33, 5, 76),
(34, 5, 77),
(35, 5, 78),
(36, 5, 79),
(102, 4, 81),
(122, 9, 81),
(63, 4, 82),
(119, 9, 82),
(65, 4, 87),
(121, 9, 87),
(101, 4, 89),
(37, 3, 90),
(38, 3, 91),
(39, 3, 92),
(40, 3, 93),
(41, 3, 94),
(42, 3, 95),
(132, 9, 95),
(43, 3, 96),
(44, 3, 97),
(45, 3, 98),
(46, 3, 99),
(47, 3, 100),
(48, 3, 101),
(49, 3, 102),
(50, 3, 103),
(51, 3, 104),
(52, 3, 105),
(53, 3, 106),
(54, 3, 107),
(55, 3, 108),
(56, 3, 109),
(57, 3, 110),
(59, 3, 111),
(60, 3, 112),
(61, 3, 113),
(123, 9, 113),
(62, 3, 114),
(58, 3, 115),
(66, 4, 117),
(67, 4, 150),
(68, 4, 151),
(131, 9, 151),
(69, 4, 152),
(127, 9, 152),
(70, 4, 153),
(71, 4, 154),
(72, 4, 155),
(73, 4, 156),
(74, 4, 157),
(75, 4, 158),
(76, 4, 159),
(77, 4, 160),
(78, 4, 161),
(80, 4, 162),
(125, 9, 162),
(82, 4, 163),
(83, 4, 164),
(84, 4, 165),
(85, 4, 166),
(86, 4, 167),
(87, 4, 168),
(88, 4, 169),
(89, 4, 170),
(90, 4, 171),
(91, 4, 172),
(92, 4, 173),
(93, 4, 174),
(94, 4, 175),
(95, 4, 176),
(96, 4, 177),
(97, 4, 178),
(98, 4, 179),
(99, 4, 180),
(100, 4, 181),
(130, 9, 182),
(118, 9, 183),
(116, 7, 184),
(107, 6, 185),
(108, 6, 186),
(103, 6, 187),
(104, 6, 188),
(105, 6, 189),
(106, 6, 190),
(109, 6, 191),
(110, 6, 192),
(111, 6, 193),
(112, 6, 194),
(115, 7, 194),
(120, 9, 194),
(113, 7, 195),
(114, 7, 196),
(124, 9, 513),
(126, 9, 582),
(117, 9, 951);

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `wm_formula2challenge`
--
ALTER TABLE `wm_formula2challenge`
  ADD CONSTRAINT `wm_formula2challenge_ibfk_1` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `wm_formula2challenge_ibfk_2` FOREIGN KEY (`challenge_id`) REFERENCES `wm_challenges` (`id`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
