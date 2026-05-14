-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 13, 2026 at 03:33 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cinema_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE `movies` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `genre` varchar(50) NOT NULL,
  `movie_year` int(11) NOT NULL,
  `description` text DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movies`
--

INSERT INTO `movies` (`id`, `title`, `genre`, `movie_year`, `description`, `image`) VALUES
(5, 'Titanic', 'Romance_horror', 2000, 'None', 'titanic-meme-8.jpg'),
(6, 'Advenger', 'Sci_fi', 2023, 'None', 'p8815512_p_v10_ap.jpg'),
(7, 'Blades of the Guardians', 'Action', 2025, 'None', 'MV5BZTM5MTY3NjQtOWUxYS00YzJiLWJiZGEtMDZmZWY3ZGZkN2MwXkEyXkFqcGc._V1_.jpg'),
(8, 'Battle at lake chnagjin', 'Action', 2025, 'None', 'lake-changjin.webp'),
(10, 'Spider-Man NowayHome', 'Action', 2021, 'None', '33e5a20674b21fd129b7dddfbf230a2d.jpg'),
(11, 'Harry Potter ', 'Adventure', 2007, 'None', '53edd39303ddae10c72993578dcc2420.jpg'),
(12, 'Avatar: Fire and Ash', 'Adventure', 2025, 'None', 'fc64f4ef0381331d52a80b204ce75749.jpg'),
(13, 'True Beauty', 'Drama', 2021, 'None', '00ec0b03efc08794fa3088ea3e8461a8.jpg'),
(14, 'My Love', 'Drama', 2021, 'None', 'a34ecfe4e4f8f43174f58109dabac9ab.jpg'),
(15, 'The Minions ', 'Comedy', 2015, 'None', '16e49d5c5dbb4021fefe94ac712d1948.jpg'),
(16, 'The Boss Baby', 'Comedy', 2017, 'None', 'c076f4df8b8a91d4e98a9ef43189611b.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(20) DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
(1, 'admin', '1234', 'admin'),
(2, 'user1', '1234', 'user'),
(3, 'homie', '123', 'user'),
(4, 'admin2', '1234', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `movies`
--
ALTER TABLE `movies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
