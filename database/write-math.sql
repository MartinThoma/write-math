-- phpMyAdmin SQL Dump
-- version 4.0.6deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 27. Apr 2014 um 18:39
-- Server Version: 5.5.35-0ubuntu0.13.10.2
-- PHP-Version: 5.5.3-1ubuntu2.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

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
  `description` text NOT NULL,
  `formula_in_latex` text NOT NULL,
  `svg` text NOT NULL,
  `is_single_symbol` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=57 ;

--
-- Daten für Tabelle `wm_formula`
--

INSERT INTO `wm_formula` (`id`, `formula_name`, `description`, `formula_in_latex`, `svg`, `is_single_symbol`) VALUES
(31, 'A', 'Single symbol ''A''', 'A', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.32125"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">A</tspan></text>\n</g></svg>', 1),
(32, 'B', 'Single symbol ''B''', 'B', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="13.8025"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">B</tspan></text>\n</g></svg>', 1),
(33, 'C', 'Single symbol ''C''', 'C', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="13.975"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">C</tspan></text>\n</g></svg>', 1),
(34, 'D', 'Single symbol ''D''', 'D', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.49375"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">D</tspan></text>\n</g></svg>', 1),
(35, 'E', 'Single symbol ''E''', 'E', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="13.45625"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">E</tspan></text>\n</g></svg>', 1),
(36, 'F', 'Single symbol ''F''', 'F', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="13.11"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">F</tspan></text>\n</g></svg>', 1),
(37, 'G', 'Single symbol ''G''', 'G', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.75375"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">G</tspan></text>\n</g></svg>', 1),
(38, 'H', 'Single symbol ''H''', 'H', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.32125"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">H</tspan></text>\n</g></svg>', 1),
(39, 'I', 'Single symbol ''I''', 'I', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="9.4787502"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">I</tspan></text>\n</g></svg>', 1),
(40, 'J', 'Single symbol ''J''', 'J', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="11.38125"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">J</tspan></text>\n</g></svg>', 1),
(41, 'K', 'Single symbol ''K''', 'K', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.6675"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">K</tspan></text>\n</g></svg>', 1),
(42, 'L', 'Single symbol ''L''', 'L', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="12.765"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">L</tspan></text>\n</g></svg>', 1),
(43, 'M', 'Single symbol ''M''', 'M', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="16.39625"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">M</tspan></text>\n</g></svg>', 1),
(44, 'N', 'Single symbol ''N''', 'N', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.32125"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">N</tspan></text>\n</g></svg>', 1),
(45, 'O', 'Single symbol ''O''', 'O', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.6675"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">O</tspan></text>\n</g></svg>', 1),
(46, 'P', 'Single symbol ''P''', 'P', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="13.45625"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">P</tspan></text>\n</g></svg>', 1),
(47, 'Q', 'Single symbol ''Q''', 'Q', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.6675"\n   height="15.9125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,15.9125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,3.93)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">Q</tspan></text>\n</g></svg>', 1),
(48, 'R', 'Single symbol ''R''', 'R', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.14875"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">R</tspan></text>\n</g></svg>', 1),
(49, 'S', 'Single symbol ''S''', 'S', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="11.9"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">S</tspan></text>\n</g></svg>', 1),
(50, 'T', 'Single symbol ''T''', 'T', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="13.975"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">T</tspan></text>\n</g></svg>', 1),
(51, 'U', 'Single symbol ''U''', 'U', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.32125"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">U</tspan></text>\n</g></svg>', 1),
(52, 'V', 'Single symbol ''V''', 'V', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.32125"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">V</tspan></text>\n</g></svg>', 1),
(53, 'W', 'Single symbol ''W''', 'W', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="17.780001"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">W</tspan></text>\n</g></svg>', 1),
(54, 'X', 'Single symbol ''X''', 'X', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.32125"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">X</tspan></text>\n</g></svg>', 1),
(55, 'Y', 'Single symbol ''Y''', 'Y', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="14.32125"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">Y</tspan></text>\n</g></svg>', 1),
(56, 'Z', 'Single symbol ''Z''', 'Z', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   version="1.1"\n   width="12.59125"\n   height="13.49125"\n   id="svg2"\n   xml:space="preserve"><metadata\n     id="metadata8"><rdf:RDF><cc:Work\n         rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" /></cc:Work></rdf:RDF></metadata><defs\n     id="defs6" /><g\n     transform="matrix(1.25,0,0,-1.25,0,13.49125)"\n     id="g10"><text\n       transform="matrix(1,0,0,-1,1.993,1.993)"\n       id="text12"><tspan\n         x="0"\n         y="0"\n         id="tspan14"\n         style="font-size:9.96259975px;font-variant:normal;font-weight:normal;writing-mode:lr-tb;fill:#000000;fill-opacity:1;fill-rule:nonzero;stroke:none;font-family:CMR10;-inkscape-font-specification:CMR10">Z</tspan></text>\n</g></svg>', 1);

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Daten für Tabelle `wm_users`
--

INSERT INTO `wm_users` (`id`, `display_name`, `email`, `password`, `salt`) VALUES
(10, 'Martin Thoma', 'info@martin-thoma.de', '47b6f579f3a6a9ed83cfed4408851ca5', 'RNWzQhFp');

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
