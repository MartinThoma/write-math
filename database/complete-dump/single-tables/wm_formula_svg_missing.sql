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

--
-- Daten für Tabelle `wm_formula_svg_missing`
--

INSERT INTO `wm_formula_svg_missing` (`id`, `user_id`, `formula_id`, `time`, `useragent`, `problem_type`) VALUES
(244, 10, 278, '2014-05-22 08:25:45', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36', 'svg missing'),
(246, 15, 1170, '2014-05-23 22:11:08', 'Mozilla/5.0 (Android; Tablet; rv:29.0) Gecko/29.0 Firefox/29.0', 'rendering wrong'),
(247, 46, 1144, '2014-05-23 22:15:55', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/6.1.3 Safari/537.75.14', 'svg missing'),
(248, 46, 917, '2014-05-23 22:22:35', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/6.1.3 Safari/537.75.14', 'svg missing'),
(249, 46, 376, '2014-05-23 22:26:11', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/6.1.3 Safari/537.75.14', 'svg missing'),
(250, 46, 915, '2014-05-24 11:03:17', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/6.1.3 Safari/537.75.14', 'svg missing'),
(251, 46, 987, '2014-05-24 11:04:30', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/6.1.3 Safari/537.75.14', 'svg missing'),
(252, 46, 292, '2014-05-24 11:08:57', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/6.1.3 Safari/537.75.14', 'svg missing'),
(253, 50, 278, '2014-05-24 16:09:50', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'svg missing'),
(254, 50, 329, '2014-05-24 16:14:28', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(255, 50, 297, '2014-05-24 16:15:16', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(256, 50, 454, '2014-05-24 16:18:36', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(257, 50, 414, '2014-05-24 16:23:01', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(258, 50, 456, '2014-05-24 16:24:35', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(259, 50, 932, '2014-05-24 16:28:44', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(260, 50, 781, '2014-05-24 16:30:42', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(261, 50, 1181, '2014-05-24 16:31:58', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(262, 50, 287, '2014-05-24 16:35:19', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(263, 50, 1091, '2014-05-24 16:35:30', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(264, 50, 936, '2014-05-24 16:39:56', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(265, 50, 896, '2014-05-24 16:40:19', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong'),
(266, 50, 584, '2014-05-24 16:52:43', 'Mozilla/5.0 (Linux; Android 4.3; SM-P600 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Safari/537.36', 'rendering wrong');

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `wm_formula_svg_missing`
--
ALTER TABLE `wm_formula_svg_missing`
  ADD CONSTRAINT `wm_formula_svg_missing_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wm_formula_svg_missing_ibfk_2` FOREIGN KEY (`formula_id`) REFERENCES `wm_formula` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
