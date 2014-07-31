-- phpMyAdmin SQL Dump
-- version 3.5.4
-- http://www.phpmyadmin.net
--
-- Host: 134.0.30.203:3306
-- Erstellungszeit: 31. Jul 2014 um 17:44
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
-- Daten für Tabelle `wm_workers`
--

INSERT INTO `wm_workers` (`id`, `user_id`, `API_key`, `worker_name`, `description`, `url`, `latest_heartbeat`, `status`) VALUES
(4, 10, '5373c82a78230', 'DTW', 0x5468697320636c69656e74206170706c69657320612044545720746563686e697175652e, 'http://www.martin-thoma.de/write-math/clients/dtw-php/', '2014-06-29 15:33:50', 'active'),
(6, 10, '5391dae1c8e99', 'DTW-Python', '', 'http://2e66a37b.ngrok.com/dtw-python/', '2014-06-06 17:39:17', 'deactivated');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
