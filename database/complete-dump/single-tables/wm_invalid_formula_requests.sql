-- phpMyAdmin SQL Dump
-- version 3.5.4
-- http://www.phpmyadmin.net
--
-- Host: 134.0.30.203:3306
-- Erstellungszeit: 17. Jul 2014 um 20:12
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

--
-- Daten für Tabelle `wm_invalid_formula_requests`
--

INSERT INTO `wm_invalid_formula_requests` (`id`, `last_request_time`, `requests`, `latex`) VALUES
(3, '2014-06-21 11:27:16', 4, '$\\subseteq$'),
(4, '2014-06-25 08:17:25', 4, '$\\Omega$'),
(5, '2014-05-29 11:44:12', 2, '\\bat');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
