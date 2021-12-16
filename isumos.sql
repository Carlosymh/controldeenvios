-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-12-2021 a las 23:34:57
-- Versión del servidor: 10.4.21-MariaDB
-- Versión de PHP: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `isumos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrada_fc`
--

CREATE TABLE `entrada_fc` (
  `ID_E_fc` bigint(100) NOT NULL,
  `Fulfillment` varchar(250) NOT NULL,
  `Pallets_Totales_Recibidos` bigint(110) NOT NULL,
  `Pallets_en_buen_estado` bigint(110) NOT NULL,
  `Pallets_en_mal_estado` bigint(110) NOT NULL,
  `Gaylords_Totales_Recibidos` bigint(110) NOT NULL,
  `Gaylords_en_buen_estado` bigint(110) NOT NULL,
  `Gaylords_en_mal_estado` bigint(110) NOT NULL,
  `Cajas` bigint(110) NOT NULL,
  `Costales` bigint(110) NOT NULL,
  `Centro_de_trabajo_origen` varchar(250) NOT NULL,
  `Cross_Dock_origen` varchar(250) NOT NULL,
  `Service_Center_Origen` varchar(250) NOT NULL,
  `Responsable` varchar(250) NOT NULL,
  `Fecha_Creación` date NOT NULL,
  `Fecha_Hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `entrada_fc`
--

INSERT INTO `entrada_fc` (`ID_E_fc`, `Fulfillment`, `Pallets_Totales_Recibidos`, `Pallets_en_buen_estado`, `Pallets_en_mal_estado`, `Gaylords_Totales_Recibidos`, `Gaylords_en_buen_estado`, `Gaylords_en_mal_estado`, `Cajas`, `Costales`, `Centro_de_trabajo_origen`, `Cross_Dock_origen`, `Service_Center_Origen`, `Responsable`, `Fecha_Creación`, `Fecha_Hora`) VALUES
(19, 'Mega parck', 390, 390, 0, 0, 0, 0, 0, 0, 'Cross Dock', 'México MXXEM1', 'N/A', 'Jessica Margarito Garduño', '2021-09-22', '2021-09-22 13:09:36'),
(392, 'Odonnell', 2, 3, 4, 4, 6, 6, 7, 7, 'Service Center', 'N/A', 'N/A', 'Carlos Yovani Muñoz Hernandez ', '2021-11-09', '2021-11-09 13:51:10'),
(393, 'Odonnell', 50, 40, 10, 46, 45, 1, 40, 20, 'Cross Dock', 'Monterrey MXXMT1', 'N/A', 'Carlos Yovani Muñoz Hernandez ', '2021-11-20', '2021-11-20 19:30:00'),
(394, 'Odonnell', 60, 60, 0, 7, 7, 0, 50, 39, 'Cross Dock', 'Guadalajara MXXGD1', 'CDMX6  SMX6', 'Carlos Yovani Muñoz Hernandez ', '2021-11-29', '2021-11-29 16:14:35'),
(395, 'Odonnell', 5, 3, 2, 9, 3, 6, 34, 90, 'Cross Dock', 'Monterrey MXXMT1', 'N/A', 'Carlos Yovani Muñoz Hernandez ', '2021-11-29', '2021-11-29 16:14:56'),
(396, 'Odonnell', 6, 3, 3, 6, 3, 3, 32, 20, 'Cross Dock', 'Guadalajara MXXGD1', 'Ciudad Victoria SVM1', 'Carlos Yovani Muñoz Hernandez ', '2021-12-07', '2021-12-07 19:42:10');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrada_svcs`
--

CREATE TABLE `entrada_svcs` (
  `ID_E_svcs` bigint(100) NOT NULL,
  `Centro_de_trabajo_donde_te_encuentras` varchar(255) NOT NULL,
  `Pallets_Totales_Recibidos` bigint(110) NOT NULL,
  `Pallets_en_buen_estado` bigint(110) NOT NULL,
  `Pallets_en_mal_estado` bigint(110) NOT NULL,
  `Gaylords_Totales_Recibidos` bigint(110) NOT NULL,
  `Gaylords_en_buen_estado` bigint(110) NOT NULL,
  `Gaylords_en_mal_estado` bigint(110) NOT NULL,
  `Cajas` bigint(110) NOT NULL,
  `Costales` bigint(110) NOT NULL,
  `Centro_de_Origen` varchar(11) NOT NULL,
  `Responsable` varchar(250) NOT NULL,
  `Fecha_Creación` date NOT NULL,
  `Fecha_Hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `entrada_svcs`
--

INSERT INTO `entrada_svcs` (`ID_E_svcs`, `Centro_de_trabajo_donde_te_encuentras`, `Pallets_Totales_Recibidos`, `Pallets_en_buen_estado`, `Pallets_en_mal_estado`, `Gaylords_Totales_Recibidos`, `Gaylords_en_buen_estado`, `Gaylords_en_mal_estado`, `Cajas`, `Costales`, `Centro_de_Origen`, `Responsable`, `Fecha_Creación`, `Fecha_Hora`) VALUES
(5, 'CDMX1 SMX1', 1, 1, 1, 1, 1, 1, 1, 1, 'Fulfillment', 'Jessica Margarito Garduño', '2021-08-30', '0000-00-00 00:00:00'),
(6, 'Odonnell', 3, 2, 1, 5, 4, 1, 45, 20, 'Cross Dock', 'Carlos Yovani Muñoz Hernandez ', '2021-11-20', '2021-11-20 18:10:44');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrada_tranferencias_fc`
--

CREATE TABLE `entrada_tranferencias_fc` (
  `ID_ET_fc` bigint(110) NOT NULL,
  `Fulfillment` varchar(250) NOT NULL,
  `Pallets` bigint(110) NOT NULL,
  `Fulfillment_origen` varchar(250) NOT NULL,
  `Responsable` varchar(250) NOT NULL,
  `Fecha_Creación` date NOT NULL,
  `Fecha_Hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `entrada_tranferencias_fc`
--

INSERT INTO `entrada_tranferencias_fc` (`ID_ET_fc`, `Fulfillment`, `Pallets`, `Fulfillment_origen`, `Responsable`, `Fecha_Creación`, `Fecha_Hora`) VALUES
(4, 'Prologis', 57, 'O\'donnell', 'Carlos Yovani', '2021-08-29', '0000-00-00 00:00:00'),
(5, 'Odonnell', 50, 'Prologis', 'Carlos Yovani Muñoz Hernandez ', '2021-11-20', '2021-11-20 20:02:08');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrada_xd`
--

CREATE TABLE `entrada_xd` (
  `ID_E_xd` bigint(110) NOT NULL,
  `Centro_de_trabajo_donde_te_encuentras` varchar(250) NOT NULL,
  `Total_tarimas` bigint(110) NOT NULL,
  `Tarima_en_buen_estado` bigint(110) NOT NULL,
  `Tarimas_en_mal_estado` bigint(110) NOT NULL,
  `Total_Gaylors` bigint(110) NOT NULL,
  `Gaylors_en_buen_estado` bigint(110) NOT NULL,
  `Gaylors_en_mal_estado` bigint(110) NOT NULL,
  `cajas` bigint(110) NOT NULL,
  `Costales` bigint(110) NOT NULL,
  `Destino_Proveniente` varchar(250) NOT NULL,
  `Responsable` varchar(250) NOT NULL,
  `Fecha_Creación` date NOT NULL,
  `Fecha_Hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `entrada_xd`
--

INSERT INTO `entrada_xd` (`ID_E_xd`, `Centro_de_trabajo_donde_te_encuentras`, `Total_tarimas`, `Tarima_en_buen_estado`, `Tarimas_en_mal_estado`, `Total_Gaylors`, `Gaylors_en_buen_estado`, `Gaylors_en_mal_estado`, `cajas`, `Costales`, `Destino_Proveniente`, `Responsable`, `Fecha_Creación`, `Fecha_Hora`) VALUES
(4, 'Culiacán MXXCU1', 10, 5, 5, 5, 5, 0, 32, 1, 'Cross Dock', 'Carlos Yovani', '2021-08-29', '0000-00-00 00:00:00'),
(5, 'México MXXEM1', 2, 2, 2, 2, 2, 2, 20, 2, 'Cross Dock', 'MASTER OF THE CAOS', '2021-10-02', '0000-00-00 00:00:00'),
(6, 'Odonnell', 25, 20, 5, 40, 30, 35, 3, 3, 'Service Center', 'Carlos Yovani Muñoz Hernandez ', '2021-11-21', '2021-11-21 21:02:02');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordenes_no_procesables`
--

CREATE TABLE `ordenes_no_procesables` (
  `id_orden` bigint(100) NOT NULL,
  `usuario_wms` varchar(255) NOT NULL,
  `paquetera` varchar(255) NOT NULL,
  `orden` bigint(100) NOT NULL,
  `pallet` varchar(255) NOT NULL,
  `tipo` varchar(255) NOT NULL,
  `fulfillment_origen` varchar(255) NOT NULL,
  `estatus` varchar(255) DEFAULT NULL,
  `service_center` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL,
  `ticket` varchar(255) NOT NULL,
  `fecha_ticket` date NOT NULL,
  `estatus_orden` varchar(250) DEFAULT NULL,
  `Comentario` varchar(255) DEFAULT NULL,
  `semana` int(70) DEFAULT NULL,
  `mes` varchar(250) DEFAULT NULL,
  `responsable` varchar(255) DEFAULT NULL,
  `fecha_actualizacion` datetime DEFAULT NULL,
  `responsable_actualizacion` varchar(255) DEFAULT NULL,
  `fecha_hora` datetime NOT NULL,
  `fecha` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `ordenes_no_procesables`
--

INSERT INTO `ordenes_no_procesables` (`id_orden`, `usuario_wms`, `paquetera`, `orden`, `pallet`, `tipo`, `fulfillment_origen`, `estatus`, `service_center`, `region`, `ticket`, `fecha_ticket`, `estatus_orden`, `Comentario`, `semana`, `mes`, `responsable`, `fecha_actualizacion`, `responsable_actualizacion`, `fecha_hora`, `fecha`) VALUES
(6, 'cmunos', 'DHL', 808082, 'PS-0-023-00-00-00', 'Devolución', 'Odonnell', 'Document', 'SMX5', '', '076006', '2021-10-21', 'Pendiente', NULL, 42, 'October', NULL, NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-10-18 15:49:19', '2021-10-18'),
(12, 'jmargarito', 'Estafeta', 31287493827192, 'PL-0-540-00-00', 'Retorno', 'Odonnell', 'Document', 'SCJ1', '', '123456', '2021-10-19', 'Cerrado', 'Se Reagendo La Entrega ', 42, 'October', NULL, '2021-11-28 19:31:48', 'Carlos Yovani Muñoz Hernandez ', '2021-10-19 15:24:39', '2021-10-19'),
(14, 'admin', '99 Minutos', 97248, 'PL-0-540-00-00', 'Retorno', 'Odonnell', 'Cancelado', 'SAG1', 'Bajio', '076006', '2021-11-18', 'Cerrado', NULL, 46, 'Noviebre', NULL, '2021-12-09 18:14:44', 'Carlos Yovani Muñoz Hernandez ', '2021-11-21 19:34:32', '2021-11-21'),
(16, 'admin', '99 Minutos', 808686, 'PS-0-023-00-00-00', 'Retorno', 'Odonnell', 'Cancelado', 'SAG1', 'Bajio', 'shpp-0183', '2021-11-10', 'Pendiente', NULL, 46, 'Noviebre', NULL, NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-11-21 19:38:51', '2021-11-21'),
(17, 'admin', '99 Minutos', 12947, 'PL-234-980-00-02', 'Retorno', 'Odonnell', 'Paquete vacio al arribo', 'SAG1', 'Bajio', '123456', '2021-11-26', 'Pendiente', 'Faltamte de Origen', 47, 'Noviebre', NULL, NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-11-23 17:11:28', '2021-11-23');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `planing`
--

CREATE TABLE `planing` (
  `id_planing` bigint(100) NOT NULL,
  `Fecha_agendada` date NOT NULL,
  `codigo_sku` bigint(200) NOT NULL,
  `descripción` varchar(255) NOT NULL,
  `piezas_p` bigint(150) NOT NULL,
  `unidades` bigint(150) NOT NULL,
  `datos_de_la_unidad` varchar(255) NOT NULL,
  `operador` varchar(255) NOT NULL,
  `origen` varchar(255) NOT NULL,
  `destino` varchar(255) NOT NULL,
  `reponsable` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `hora_inicio_de_carga` datetime DEFAULT NULL,
  `hora_de_despacho` datetime DEFAULT NULL,
  `marchamo` bigint(100) DEFAULT NULL,
  `marchamo2` bigint(100) DEFAULT NULL,
  `arribo_a_fc_destino` datetime DEFAULT NULL,
  `responsable_fc` varchar(255) DEFAULT NULL,
  `responsable_xd` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `planing`
--

INSERT INTO `planing` (`id_planing`, `Fecha_agendada`, `codigo_sku`, `descripción`, `piezas_p`, `unidades`, `datos_de_la_unidad`, `operador`, `origen`, `destino`, `reponsable`, `status`, `hora_inicio_de_carga`, `hora_de_despacho`, `marchamo`, `marchamo2`, `arribo_a_fc_destino`, `responsable_fc`, `responsable_xd`) VALUES
(13, '2021-09-20', 10060, 'Tarima de Madera', 390, 1, 'N/A', 'N/A', 'Cross Dock', 'Prologis', 'Jessica Margarito Garduño', 'Recibido', '2021-09-29 19:54:43', '2021-09-29 19:54:54', 5802, 4589, '2021-09-29 19:56:50', 'MASTER OF THE CAOS', 'MASTER OF THE CAOS'),
(14, '2021-09-20', 10060, 'Tarima de Madera', 390, 1, 'N/A', 'N/A', 'Cross Dock', 'Mega Park', 'Jessica Margarito Garduño', 'Recibido', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(43, '2021-11-17', 10053, 'Caja Gaylord', 40, 1, 'Unidad 514', 'juancho', 'Service Center', 'Odonnell', 'Carlos Yovani Muñoz Hernandez ', 'Enviado', '2021-11-28 17:40:43', '2021-11-28 17:45:52', 556, 4589, '2021-11-28 17:58:47', 'Carlos Yovani Muñoz Hernandez ', 'Carlos Yovani Muñoz Hernandez '),
(44, '2021-11-30', 10060, 'Tarima Madera', 50, 1, 'trailer matricula 5646jkg', 'David Godínez Fentes', 'Service Center', 'CPA Logistics Center', 'Carlos Yovani Muñoz Hernandez ', 'Pendiente', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(45, '2021-11-30', 10060, 'Tarima Madera', 50, 1, 'trailer matricula 5646jkg', 'David Godínez Fentes', 'Service Center', 'CPA Logistics Center', 'Carlos Yovani Muñoz Hernandez ', 'Pendiente', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prealert`
--

CREATE TABLE `prealert` (
  `ID_Prealert` bigint(255) NOT NULL,
  `ID_Envio_Prealert` varchar(255) NOT NULL,
  `Origen` varchar(255) NOT NULL,
  `SiteName` varchar(255) NOT NULL,
  `Destino` varchar(255) NOT NULL,
  `SiteName_Destino` varchar(255) NOT NULL,
  `EmpresaTransporte` varchar(255) NOT NULL,
  `Transportista` varchar(255) NOT NULL,
  `Placas` varchar(255) NOT NULL,
  `Orden` bigint(255) DEFAULT NULL,
  `Paquetera` varchar(255) DEFAULT NULL,
  `Marchamo` varchar(255) DEFAULT NULL,
  `Responsable` varchar(255) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `fecha_hora` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `prealert`
--

INSERT INTO `prealert` (`ID_Prealert`, `ID_Envio_Prealert`, `Origen`, `SiteName`, `Destino`, `SiteName_Destino`, `EmpresaTransporte`, `Transportista`, `Placas`, `Orden`, `Paquetera`, `Marchamo`, `Responsable`, `Fecha`, `fecha_hora`) VALUES
(1, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXEM1', 'Eurologistics', 'juanito perez', 'KMJ026', 58757, 'Mercado Envíos', NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-12-12', '2021-12-12 18:50:48'),
(3, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXGD1', 'TMS', 'yovani', 'hujl48945', 8964, 'Estafeta', NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-12-12', '2021-12-12 19:13:18'),
(4, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXGD1', 'TMS', 'yovani', 'hujl48945', 8698635, 'DHL', NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-12-12', '2021-12-12 19:13:32'),
(5, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXGD1', 'TMS', 'yovani', 'hujl48945', 45675, 'Paquetexpress', NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-12-12', '2021-12-12 19:13:43'),
(6, 'CE20211213134242461652P', 'Cross Dock', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'yovani', 'KMJ026', 483454, 'DHL', NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-12-13', '2021-12-13 13:42:54'),
(7, 'CE20211213134242461652P', 'Cross Dock', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'yovani', 'KMJ026', 8434835, 'FedEx', NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-12-13', '2021-12-13 13:43:02'),
(8, 'CE20211213134242461652P', 'Cross Dock', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'yovani', 'KMJ026', 843435, '99 minutos', NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-12-13', '2021-12-13 13:43:10'),
(9, 'CE20211213134242461652P', 'Cross Dock', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'yovani', 'KMJ026', 0, 'Mercado Envíos', NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-12-13', '2021-12-13 13:43:14'),
(10, 'CE20211213195345671869P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'yovani', 'KMJ026', 25235, 'Mercado Envíos', NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-12-13', '2021-12-13 19:53:50'),
(11, 'CE20211213195345671869P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'yovani', 'KMJ026', 4265321, 'Mercado Envíos', NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-12-13', '2021-12-13 19:53:56'),
(12, 'CE20211213195345671869P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'yovani', 'KMJ026', 2135, 'Mercado Envíos', NULL, 'Carlos Yovani Muñoz Hernandez ', '2021-12-13', '2021-12-13 19:54:00'),
(13, 'CE20211214155931398528P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'juanito perez', 'KMJ026', 86584, 'Paquetexpress', '7957854', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 15:59:39'),
(14, 'CE20211214155931398528P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'juanito perez', 'KMJ026', 9758674, 'FedEx', '7957854', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 15:59:46'),
(15, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'juanito perez', 'KMJ026', 346775, 'Paquetexpress', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 16:41:34'),
(16, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'juanito perez', 'KMJ026', 483286, 'Paquetexpress', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 16:41:41'),
(17, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'juanito perez', 'KMJ026', 4288856, '99 minutos', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 16:41:49'),
(18, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'juanito perez', 'KMJ026', 8698643, '99 minutos', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 16:41:57'),
(19, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Fullfilment', 'FCJC01', 'Eurologistics', 'yovani', 'KMJ026', 8346685235, 'Paquetexpress', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 16:44:09'),
(20, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Fullfilment', 'FCD02', 'TMS', 'Cesar Perez', 'jhfd9854', 684831, 'Estafeta', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 16:48:26'),
(21, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Fullfilment', 'FCD02', 'TMS', 'Cesar Perez', 'jhfd9854', 863140, '99 minutos', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 16:49:28'),
(22, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Fullfilment', 'FCD02', 'TMS', 'Cesar Perez', 'jhfd9854', 978623, 'Estafeta', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 16:49:35'),
(23, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Fullfilment', 'FCD03', 'TMS', 'yovani', 'cdd6788', 86143, 'FedEx', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 16:59:01'),
(24, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Fullfilment', 'FCD03', 'TMS', 'yovani', 'cdd6788', 31526, 'Estafeta', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 16:59:09'),
(25, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'FCD03', 'TMS', 'yovani', 'cdd6788', 3236, 'Mercado Envíos', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:02:50'),
(26, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Fullfilment', 'FCD04', 'TMS', 'yovani', 'KMJ026', 79587, 'Mercado Envíos', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:06:06'),
(27, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'FCD04', 'TMS', 'yovani', 'KMJ026', 436, 'Mercado Envíos', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:19:24'),
(28, 'CE20211212185012841326P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'FCD04', 'TMS', 'yovani', 'KMJ026', 3477385, 'Mercado Envíos', '757532', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:22:53'),
(29, 'CE20211214155931398528P', 'Fullfilment', 'Odonnell', 'Fullfilment', 'FCD03', 'TMS', 'juanito perez', 'KMJ026', 925632, 'Mercado Envíos', '7957854', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:29:27'),
(30, 'CE20211214155931398528P', 'Fullfilment', 'Odonnell', 'Fullfilment', 'FCD03', 'TMS', 'juanito perez', 'KMJ026', 125153, 'DHL', '7957854', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:29:32'),
(31, 'CE20211214155931398528P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'FCD03', 'TMS', 'juanito perez', 'KMJ026', 864, 'Mercado Envíos', '7957854', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:40:58'),
(32, 'CE20211214155931398528P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'FCD03', 'TMS', 'juanito perez', 'KMJ026', 647635, 'Mercado Envíos', '7957854', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:42:08'),
(33, 'CE20211214155931398528P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'FCD03', 'TMS', 'juanito perez', 'KMJ026', 7467353, 'Paquetexpress', '7957854', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:42:14'),
(34, 'CE20211214155931398528P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'FCD03', 'TMS', 'juanito perez', 'KMJ026', 3537437, 'Paquetexpress', '7957854', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:45:18'),
(35, 'CE20211214155931398528P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXMT1', 'Eurologistics', 'yovani', 'KMJ026', 3646, 'Estafeta', '7957854', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:48:42'),
(36, 'CE20211214155931398528P', 'Fullfilment', 'Odonnell', 'Fullfilment', 'FCD03', 'TMS', 'yovani', 'cdd6788', 43727, 'FedEx', '7957854', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 17:49:38'),
(37, 'CE20211214155931398528P', 'Fullfilment', 'Odonnell', 'Cross Dock', 'MXXEM1', 'TMS', 'yovani', 'hvas08213', 785875, 'Mercado Envíos', '7957854', 'Carlos Yovani Muñoz Hernandez ', '2021-12-14', '2021-12-14 18:01:20'),
(41, 'CE20211215140246052791P', 'Fullfilment', 'Odonnell', 'Fullfilment', 'FCD04', 'Eurologistics', 'pedro pica piedra', 'MKdir0903', 97587532, 'Paquetexpress', '110033', 'Carlos Yovani Muñoz Hernandez ', '2021-12-15', '2021-12-15 17:23:13');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recibo_fc`
--

CREATE TABLE `recibo_fc` (
  `ID_Recibo` bigint(50) NOT NULL,
  `ID_Envio_Prealert` varchar(255) NOT NULL,
  `Orden` bigint(255) NOT NULL,
  `Paquetera` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `Comentario` varchar(255) NOT NULL,
  `Facility` varchar(255) NOT NULL,
  `SiteName` varchar(255) NOT NULL,
  `Responsable` varchar(255) NOT NULL,
  `Fecha` date NOT NULL,
  `Fecha_Hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `recibo_fc`
--

INSERT INTO `recibo_fc` (`ID_Recibo`, `ID_Envio_Prealert`, `Orden`, `Paquetera`, `status`, `Comentario`, `Facility`, `SiteName`, `Responsable`, `Fecha`, `Fecha_Hora`) VALUES
(1, 'CE20211215140246052791P', 8689634, 'Paquetexpress', '', '', 'Fullfilment', 'Odonnell', 'Carlos Yovani Muñoz Hernandez ', '2021-12-15', '2021-12-15 19:36:45'),
(2, 'CE20211215140246052791P', 958746, 'FedEx', '', '', 'Fullfilment', 'Odonnell', 'Carlos Yovani Muñoz Hernandez ', '2021-12-15', '2021-12-15 19:38:02'),
(3, 'CE20211215140246052791P', 7576457, '99 minutos', '', '', 'Fullfilment', 'Odonnell', 'Carlos Yovani Muñoz Hernandez ', '2021-12-15', '2021-12-15 19:38:17'),
(4, 'CE20211215140246052791P', 97587532, 'Paquetexpress', '', '', 'Fullfilment', 'Odonnell', 'Carlos Yovani Muñoz Hernandez ', '2021-12-15', '2021-12-15 19:38:30'),
(6, 'CE20211213134242461652P', 974634, 'Estafeta', '', '', 'Fullfilment', 'Odonnell', 'Carlos Yovani Muñoz Hernandez ', '2021-12-15', '2021-12-15 20:06:21'),
(7, 'CE20211213134242461652P', 7576457, '99 minutos', '', '', 'Fullfilment', 'Odonnell', 'Carlos Yovani Muñoz Hernandez ', '2021-12-15', '2021-12-15 20:22:24'),
(9, 'CE20211213134242461652P', 8434835, 'FedEx', '', '', 'Fullfilment', 'Odonnell', 'Carlos Yovani Muñoz Hernandez ', '2021-12-15', '2021-12-15 20:24:47'),
(10, 'CE20211215140246052791P', 97575, 'Estafeta', 'Aceptado', 'Articulo en Buen estado ', 'Fullfilment', 'Odonnell', 'Fullfilment', '2021-12-16', '2021-12-16 15:17:50');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salida_fc`
--

CREATE TABLE `salida_fc` (
  `ID_S_fc` bigint(100) NOT NULL,
  `Fulfillment` varchar(250) NOT NULL,
  `Tarimas_enviadas` bigint(100) NOT NULL,
  `Gaylord_Enviados` bigint(100) NOT NULL,
  `cajas` bigint(100) NOT NULL,
  `costales` bigint(100) NOT NULL,
  `centro_de_trabajo_Destino` varchar(250) NOT NULL,
  `Service_Center` varchar(250) NOT NULL,
  `FC_Destino` varchar(250) NOT NULL,
  `Responsable` varchar(250) NOT NULL,
  `Fecha_Creación` date NOT NULL,
  `Fecha_Hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `salida_fc`
--

INSERT INTO `salida_fc` (`ID_S_fc`, `Fulfillment`, `Tarimas_enviadas`, `Gaylord_Enviados`, `cajas`, `costales`, `centro_de_trabajo_Destino`, `Service_Center`, `FC_Destino`, `Responsable`, `Fecha_Creación`, `Fecha_Hora`) VALUES
(5, 'O\'donnell', 30, 25, 45, 5, 'Fulfillment', 'N/A', 'Mega Parck', 'Carlos Yovani', '2021-09-01', '0000-00-00 00:00:00'),
(18, '', 0, 0, 0, 0, '', '', '', 'MASTER OF THE CAOS', '2021-09-26', '2021-09-26 21:08:23'),
(19, 'Prologis', 12, 12, 13, 12, 'Service Center', 'CDMX1 SMX1', 'N/A', 'Jessica Margarito Garduño', '2021-11-12', '2021-11-12 12:39:00'),
(20, 'Odonnell', 40, 50, 45, 60, 'Fulfillment', 'N/A', 'Odonnell', 'Carlos Yovani Muñoz Hernandez ', '2021-11-20', '2021-11-20 19:42:12');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salida_svcs`
--

CREATE TABLE `salida_svcs` (
  `ID_S_svcs` bigint(100) NOT NULL,
  `Centro_de_trabajo_donde_te_encuentras` varchar(255) NOT NULL,
  `Tarimas_enviadas` bigint(100) NOT NULL,
  `Gaylord_Enviados` bigint(100) NOT NULL,
  `cajas` bigint(100) NOT NULL,
  `costales` bigint(100) NOT NULL,
  `Cross_Dock` varchar(250) NOT NULL,
  `Responsable` varchar(250) NOT NULL,
  `Fecha_Creación` date NOT NULL,
  `Fecha_Hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `salida_svcs`
--

INSERT INTO `salida_svcs` (`ID_S_svcs`, `Centro_de_trabajo_donde_te_encuentras`, `Tarimas_enviadas`, `Gaylord_Enviados`, `cajas`, `costales`, `Cross_Dock`, `Responsable`, `Fecha_Creación`, `Fecha_Hora`) VALUES
(4, 'Oaxaca SOX1', 4, 5, 23, 6, 'Monterrey MXXMT1', 'Carlos Yovani', '2021-08-29', '0000-00-00 00:00:00'),
(5, 'Odonnell', 5, 6, 45, 20, 'México MXXEM1', 'Carlos Yovani Muñoz Hernandez ', '2021-11-20', '2021-11-20 18:22:39');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salida_xd`
--

CREATE TABLE `salida_xd` (
  `ID_S_xd` bigint(100) NOT NULL,
  `Centro_de_trabajo_donde_te_encuentras` varchar(250) NOT NULL,
  `Tarimas_Enviadas` bigint(100) NOT NULL,
  `Gaylord_Enviados` bigint(100) NOT NULL,
  `cajas` bigint(100) NOT NULL,
  `costales` bigint(100) NOT NULL,
  `Destino_de_la_carga` varchar(250) NOT NULL,
  `service_center` varchar(250) NOT NULL,
  `Fulfillment` varchar(250) NOT NULL,
  `Responsable` varchar(250) NOT NULL,
  `Fecha_Creación` date NOT NULL,
  `Fecha_Hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `salida_xd`
--

INSERT INTO `salida_xd` (`ID_S_xd`, `Centro_de_trabajo_donde_te_encuentras`, `Tarimas_Enviadas`, `Gaylord_Enviados`, `cajas`, `costales`, `Destino_de_la_carga`, `service_center`, `Fulfillment`, `Responsable`, `Fecha_Creación`, `Fecha_Hora`) VALUES
(6, 'México MXXEM1', 2, 2, 2, 2, 'Service Center', 'CDMX6  SMX6', 'N/A', 'Carlos Yovani', '2021-08-29', '0000-00-00 00:00:00'),
(7, 'Odonnell', 426, 442, 23, 57, 'Fulfillment', 'N/A', 'Guadalajara', 'Carlos Yovani Muñoz Hernandez ', '2021-11-23', '2021-11-23 13:07:59');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `ID` bigint(100) NOT NULL,
  `Nombre` varchar(250) NOT NULL,
  `Usuario` varchar(70) NOT NULL,
  `ltrabajo` varchar(250) NOT NULL,
  `cdt` varchar(255) NOT NULL,
  `contraseña` varchar(250) NOT NULL,
  `Rango` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`ID`, `Nombre`, `Usuario`, `ltrabajo`, `cdt`, `contraseña`, `Rango`) VALUES
(59, 'Carlos Yovani Muñoz Hernandez ', 'tcmunos', 'Fullfilment', 'Odonnell', 'pbkdf2:sha256:30$fDHpcUi46Xp6RLY4bAwqgPtagCYRNp$f5cf25f3a85b97154cced9dd91a88706efbea20154ef8dcedcfccd7017e272ac', 'Team Leader'),
(60, 'Carlos Yovani Muñoz Hernandez ', 'admin', 'Fullfilment', 'Odonnell', 'pbkdf2:sha256:30$HV3Gr1FpppJlnGIbkPcuWjBnlQ3Moq$a6609b2961f81ea59e4bb72ec5a16f828b33a39738bfb8222e7355c6a291bd05', 'Administrador'),
(61, 'Carlos Yovani Muñoz Hernandez ', 'cmunos', 'Fullfilment', 'Odonnell', 'pbkdf2:sha256:30$B2USsSBhNyzRCffKgyMbvpSMoxwEAN$f0abb1e10c3691b44893e5836021efb4f3b19e881d81e258cfd77d7405f4c8af', 'Auxiliar'),
(62, 'Carlos Yovani Muñoz Hernandez ', 'caunimun', 'Fullfilment', 'Odonnell', 'pbkdf2:sha256:30$eTWE47sPB8bxGv7i5WCN4tjBpx0zR9$1c1198ac6bf9e3658103c831a5a84f7b3898f42dbb6db5830569a6c76b42b43e', 'Representante'),
(63, 'Carlos Yovani Muñoz Hernandez ', 'vcmunos', 'Cross Dock', 'Odonnell', 'pbkdf2:sha256:30$V2xtwxe9nO7JYIjrqCLzKltanLG68n$31d5aeb41987a43b0dd68202d7b888cea91958fe04b075f9942fd5a8e8ea6abb', 'Planeacion');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `entrada_fc`
--
ALTER TABLE `entrada_fc`
  ADD PRIMARY KEY (`ID_E_fc`);

--
-- Indices de la tabla `entrada_svcs`
--
ALTER TABLE `entrada_svcs`
  ADD PRIMARY KEY (`ID_E_svcs`);

--
-- Indices de la tabla `entrada_tranferencias_fc`
--
ALTER TABLE `entrada_tranferencias_fc`
  ADD PRIMARY KEY (`ID_ET_fc`);

--
-- Indices de la tabla `entrada_xd`
--
ALTER TABLE `entrada_xd`
  ADD PRIMARY KEY (`ID_E_xd`);

--
-- Indices de la tabla `ordenes_no_procesables`
--
ALTER TABLE `ordenes_no_procesables`
  ADD PRIMARY KEY (`id_orden`);

--
-- Indices de la tabla `planing`
--
ALTER TABLE `planing`
  ADD PRIMARY KEY (`id_planing`);

--
-- Indices de la tabla `prealert`
--
ALTER TABLE `prealert`
  ADD PRIMARY KEY (`ID_Prealert`);

--
-- Indices de la tabla `recibo_fc`
--
ALTER TABLE `recibo_fc`
  ADD PRIMARY KEY (`ID_Recibo`);

--
-- Indices de la tabla `salida_fc`
--
ALTER TABLE `salida_fc`
  ADD PRIMARY KEY (`ID_S_fc`);

--
-- Indices de la tabla `salida_svcs`
--
ALTER TABLE `salida_svcs`
  ADD PRIMARY KEY (`ID_S_svcs`);

--
-- Indices de la tabla `salida_xd`
--
ALTER TABLE `salida_xd`
  ADD PRIMARY KEY (`ID_S_xd`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `entrada_fc`
--
ALTER TABLE `entrada_fc`
  MODIFY `ID_E_fc` bigint(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=397;

--
-- AUTO_INCREMENT de la tabla `entrada_svcs`
--
ALTER TABLE `entrada_svcs`
  MODIFY `ID_E_svcs` bigint(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `entrada_tranferencias_fc`
--
ALTER TABLE `entrada_tranferencias_fc`
  MODIFY `ID_ET_fc` bigint(110) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `entrada_xd`
--
ALTER TABLE `entrada_xd`
  MODIFY `ID_E_xd` bigint(110) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `ordenes_no_procesables`
--
ALTER TABLE `ordenes_no_procesables`
  MODIFY `id_orden` bigint(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `planing`
--
ALTER TABLE `planing`
  MODIFY `id_planing` bigint(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT de la tabla `prealert`
--
ALTER TABLE `prealert`
  MODIFY `ID_Prealert` bigint(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT de la tabla `recibo_fc`
--
ALTER TABLE `recibo_fc`
  MODIFY `ID_Recibo` bigint(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `salida_fc`
--
ALTER TABLE `salida_fc`
  MODIFY `ID_S_fc` bigint(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `salida_svcs`
--
ALTER TABLE `salida_svcs`
  MODIFY `ID_S_svcs` bigint(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `salida_xd`
--
ALTER TABLE `salida_xd`
  MODIFY `ID_S_xd` bigint(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `ID` bigint(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
