-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 15-09-2026 a las 14:20:37
-- Versión del servidor: 8.0.41
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `negocio`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cargos`
--

DROP TABLE IF EXISTS `cargos`;
CREATE TABLE IF NOT EXISTS `cargos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `descripcion` varchar(200) COLLATE utf8mb4_spanish_ci NOT NULL,
  `creado` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `cargos`
--

INSERT INTO `cargos` (`id`, `nombre`, `descripcion`, `creado`) VALUES
(1, 'Vendedor', 'Tipo que vende puertas', '2026-09-15 13:55:56.000000'),
(2, 'Bodeguero', 'Tipo de duerme en la bodega', '2026-09-15 13:56:19.000000'),
(3, 'Supervisor', 'Tipo que solo anda mirando', '2026-09-15 13:56:38.000000'),
(4, 'Cajero', 'Tipo que cuenta la plata y siempre le falta un peso', '2026-09-15 11:02:59.000000'),
(5, 'Conserje', 'Tipo que sabe la vida de todo el edificio', '2026-09-15 11:02:59.000000'),
(6, 'Junior', 'Tipo que camina todo el día haciendo trámites', '2026-09-15 11:02:59.000000'),
(7, 'Secretaria', 'La que realmente maneja toda la empresa', '2026-09-15 11:02:59.000000'),
(8, 'Contador', 'Tipo que sufre cada fin de mes con los balances', '2026-09-15 11:02:59.000000'),
(9, 'Informático', 'Tipo que te dice \"reinicia el equipo\" para arreglar todo', '2026-09-15 11:02:59.000000'),
(10, 'Guardia', 'Tipo que te pide el carnet aunque te vea todos los días', '2026-09-15 11:02:59.000000'),
(11, 'Repartidor', 'Tipo que llega cuando justo entraste al baño', '2026-09-15 11:02:59.000000'),
(12, 'Diseñador', 'Tipo que cambia el logo de color cinco veces al día', '2026-09-15 11:02:59.000000'),
(13, 'Gerente', 'Tipo que hace reuniones para planificar otra reunión', '2026-09-15 11:02:59.000000');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
