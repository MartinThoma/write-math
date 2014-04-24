-- phpMyAdmin SQL Dump
-- version 4.0.6deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 24. Apr 2014 um 19:04
-- Server Version: 5.5.35-0ubuntu0.13.10.2
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
-- Tabellenstruktur für Tabelle `wm_challenges`
--

CREATE TABLE IF NOT EXISTS `wm_challenges` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challange_name` varchar(255) NOT NULL,
  `formula` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_formula`
--

CREATE TABLE IF NOT EXISTS `wm_formula` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formula_name` varchar(255) NOT NULL,
  `formula_in_latex` text NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Daten für Tabelle `wm_formula`
--

INSERT INTO `wm_formula` (`id`, `formula_name`, `formula_in_latex`, `description`) VALUES
(1, '1', '1', 'The symbol ''1''.'),
(2, '2', '2', 'The symbol ''2''.');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_openid`
--

CREATE TABLE IF NOT EXISTS `wm_openid` (
  `id` int(11) NOT NULL,
  `openid_url` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `openid_url_2` (`openid_url`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_raw_draw_data`
--

CREATE TABLE IF NOT EXISTS `wm_raw_draw_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `data` text NOT NULL,
  `creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `accepted_formula_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `accepted_formula_id` (`accepted_formula_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Daten für Tabelle `wm_raw_draw_data`
--

INSERT INTO `wm_raw_draw_data` (`id`, `user_id`, `data`, `creation_date`, `accepted_formula_id`) VALUES
(2, 8, '[[{"x":253,"y":220},{"x":254,"y":217},{"x":255,"y":214},{"x":257,"y":209},{"x":259,"y":204},{"x":261,"y":198},{"x":264,"y":191},{"x":268,"y":184},{"x":272,"y":176},{"x":276,"y":168},{"x":281,"y":161},{"x":285,"y":153},{"x":290,"y":145},{"x":294,"y":137},{"x":298,"y":129},{"x":303,"y":121},{"x":307,"y":115},{"x":309,"y":110},{"x":311,"y":107},{"x":311,"y":106},{"x":312,"y":105},{"x":312,"y":107},{"x":312,"y":110},{"x":312,"y":113},{"x":312,"y":116},{"x":312,"y":123},{"x":312,"y":131},{"x":312,"y":138},{"x":312,"y":146},{"x":312,"y":155},{"x":312,"y":165},{"x":312,"y":175},{"x":312,"y":187},{"x":310,"y":199},{"x":310,"y":211},{"x":310,"y":223},{"x":308,"y":236},{"x":308,"y":248},{"x":306,"y":260},{"x":306,"y":273},{"x":304,"y":284},{"x":304,"y":295},{"x":302,"y":302},{"x":302,"y":308},{"x":302,"y":314},{"x":302,"y":318},{"x":302,"y":321},{"x":302,"y":322},{"x":302,"y":323},{"x":301,"y":323}]]', '2014-04-24 18:33:02', 1),
(4, 8, '[[{"x":232,"y":313},{"x":233,"y":311},{"x":235,"y":309},{"x":236,"y":306},{"x":238,"y":303},{"x":240,"y":300},{"x":242,"y":297},{"x":244,"y":293},{"x":247,"y":287},{"x":251,"y":282},{"x":254,"y":277},{"x":255,"y":271},{"x":259,"y":266},{"x":263,"y":260},{"x":267,"y":255},{"x":271,"y":249},{"x":275,"y":244},{"x":279,"y":238},{"x":283,"y":234},{"x":287,"y":230},{"x":291,"y":226},{"x":295,"y":224},{"x":296,"y":223},{"x":297,"y":221},{"x":298,"y":220},{"x":298,"y":219},{"x":299,"y":219},{"x":300,"y":218},{"x":300,"y":216},{"x":301,"y":215},{"x":302,"y":214},{"x":302,"y":213},{"x":302,"y":212},{"x":303,"y":212},{"x":303,"y":214},{"x":304,"y":217},{"x":304,"y":222},{"x":304,"y":228},{"x":306,"y":235},{"x":306,"y":243},{"x":306,"y":251},{"x":306,"y":260},{"x":306,"y":270},{"x":304,"y":280},{"x":304,"y":290},{"x":302,"y":300},{"x":300,"y":310},{"x":298,"y":320},{"x":297,"y":328},{"x":295,"y":336},{"x":293,"y":344},{"x":291,"y":352},{"x":291,"y":360},{"x":289,"y":369},{"x":289,"y":377},{"x":289,"y":385},{"x":288,"y":391},{"x":288,"y":397},{"x":288,"y":403},{"x":288,"y":409},{"x":288,"y":413},{"x":288,"y":416},{"x":288,"y":418},{"x":288,"y":420},{"x":288,"y":422},{"x":288,"y":423},{"x":288,"y":424}]]', '2014-04-24 18:37:40', 1),
(5, 8, '[[{"x":245,"y":299},{"x":246,"y":298},{"x":247,"y":297},{"x":249,"y":295},{"x":252,"y":294},{"x":255,"y":292},{"x":259,"y":289},{"x":265,"y":285},{"x":271,"y":280},{"x":277,"y":275},{"x":283,"y":271},{"x":290,"y":265},{"x":296,"y":259},{"x":300,"y":253},{"x":304,"y":248},{"x":308,"y":242},{"x":310,"y":236},{"x":311,"y":232},{"x":311,"y":228},{"x":312,"y":227},{"x":312,"y":229},{"x":312,"y":233},{"x":312,"y":239},{"x":312,"y":246},{"x":312,"y":254},{"x":312,"y":261},{"x":312,"y":269},{"x":311,"y":277},{"x":311,"y":287},{"x":311,"y":297},{"x":309,"y":307},{"x":309,"y":317},{"x":309,"y":327},{"x":309,"y":337},{"x":307,"y":345},{"x":307,"y":353},{"x":305,"y":361},{"x":305,"y":369},{"x":305,"y":384},{"x":305,"y":390},{"x":303,"y":396},{"x":303,"y":400},{"x":303,"y":404},{"x":303,"y":408},{"x":303,"y":412},{"x":303,"y":413},{"x":303,"y":415},{"x":303,"y":416},{"x":303,"y":417},{"x":303,"y":418},{"x":303,"y":419},{"x":303,"y":420}]]', '2014-04-24 18:41:00', 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_symbols`
--

CREATE TABLE IF NOT EXISTS `wm_symbols` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `written_name` varchar(255) CHARACTER SET utf8 NOT NULL,
  `spoken_name` varchar(255) CHARACTER SET utf8 NOT NULL,
  `latex` varchar(255) CHARACTER SET utf8 NOT NULL,
  `svg` text CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Daten für Tabelle `wm_symbols`
--

INSERT INTO `wm_symbols` (`id`, `written_name`, `spoken_name`, `latex`, `svg`) VALUES
(1, '1', 'one', '1', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\r\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\r\n\r\n<svg\r\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\r\n   xmlns:cc="http://creativecommons.org/ns#"\r\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\r\n   xmlns:svg="http://www.w3.org/2000/svg"\r\n   xmlns="http://www.w3.org/2000/svg"\r\n   version="1.1"\r\n   width="11.2075"\r\n   height="13.00625"\r\n   id="svg2"\r\n   xml:space="preserve"><metadata\r\n     id="metadata8"><rdf:RDF><cc:Work\r\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\r\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\r\n     id="defs6" /><g\r\n     transform="matrix(1.25,0,0,-1.25,0,13.00625)"\r\n     id="g10"><text\r\n       transform="matrix(1,0,0,-1,1.993,1.993)"\r\n       id="text12"><tspan\r\n         x="0"\r\n         y="0"\r\n         id="tspan14"\r\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">1</tspan></text>\r\n</g></svg>'),
(2, '2', 'two', '2', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\r\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\r\n\r\n<svg\r\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\r\n   xmlns:cc="http://creativecommons.org/ns#"\r\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\r\n   xmlns:svg="http://www.w3.org/2000/svg"\r\n   xmlns="http://www.w3.org/2000/svg"\r\n   version="1.1"\r\n   width="11.2075"\r\n   height="13.00625"\r\n   id="svg2"\r\n   xml:space="preserve"><metadata\r\n     id="metadata8"><rdf:RDF><cc:Work\r\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\r\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\r\n     id="defs6" /><g\r\n     transform="matrix(1.25,0,0,-1.25,0,13.00625)"\r\n     id="g10"><text\r\n       transform="matrix(1,0,0,-1,1.993,1.993)"\r\n       id="text12"><tspan\r\n         x="0"\r\n         y="0"\r\n         id="tspan14"\r\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">2</tspan></text>\r\n</g></svg>');

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_tag2user`
--

CREATE TABLE IF NOT EXISTS `wm_tag2user` (
  `user_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`tag_id`),
  KEY `tag_id` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_tags`
--

CREATE TABLE IF NOT EXISTS `wm_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(255) NOT NULL,
  `tag_description` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag_name` (`tag_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `wm_users`
--

CREATE TABLE IF NOT EXISTS `wm_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `display_name` varchar(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` char(32) NOT NULL,
  `salt` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `display_name` (`display_name`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Daten für Tabelle `wm_users`
--

INSERT INTO `wm_users` (`id`, `display_name`, `email`, `password`, `salt`) VALUES
(8, 'moose', 'info@martin-thoma.de', '9165028d08fd7bff5099b8973db2e3db', 'vtfzIklo');

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `wm_openid`
--
ALTER TABLE `wm_openid`
  ADD CONSTRAINT `wm_openid_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`);

--
-- Constraints der Tabelle `wm_raw_draw_data`
--
ALTER TABLE `wm_raw_draw_data`
  ADD CONSTRAINT `wm_raw_draw_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `wm_users` (`id`),
  ADD CONSTRAINT `wm_raw_draw_data_ibfk_2` FOREIGN KEY (`accepted_formula_id`) REFERENCES `wm_formula` (`id`);

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

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
