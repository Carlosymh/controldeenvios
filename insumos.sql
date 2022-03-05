-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-03-2022 a las 20:18:50
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
-- Base de datos: `insumos`
--
CREATE DATABASE IF NOT EXISTS `insumos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `insumos`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrada_svcs`
--

DROP TABLE IF EXISTS `entrada_svcs`;
CREATE TABLE `entrada_svcs` (
  `ID_E_svcs` bigint(100) NOT NULL,
  `Centro_de_trabajo_donde_te_encuentras` varchar(255) NOT NULL,
  `Pallets_Totales_Recibidos` bigint(110) NOT NULL,
  `Pallets_en_buen_estado` bigint(110) NOT NULL,
  `Pallets_en_mal_estado` bigint(110) NOT NULL,
  `Gaylords_Totales_Recibidos` bigint(110) NOT NULL,
  `Gaylords_en_buen_estado` bigint(110) NOT NULL,
  `Gaylords_en_mal_estado` bigint(110) NOT NULL,
  `Centro_de_Origen` varchar(11) NOT NULL,
  `Responsable` varchar(250) NOT NULL,
  `Fecha_Creación` date NOT NULL,
  `Fecha_Hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordenes_no_procesables`
--

DROP TABLE IF EXISTS `ordenes_no_procesables`;
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
  `ticket` varchar(255) DEFAULT NULL,
  `fecha_ticket` date DEFAULT NULL,
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

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `planing`
--

DROP TABLE IF EXISTS `planing`;
CREATE TABLE `planing` (
  `id_planing` varchar(100) NOT NULL,
  `Fecha_agendada` date NOT NULL,
  `codigo_sku` bigint(200) NOT NULL,
  `descripción` varchar(255) NOT NULL,
  `piezas_p` bigint(150) NOT NULL,
  `unidades` bigint(150) NOT NULL,
  `datos_de_la_unidad` varchar(255) DEFAULT NULL,
  `operador` varchar(255) DEFAULT NULL,
  `origen` varchar(255) DEFAULT NULL,
  `destino` varchar(255) DEFAULT NULL,
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

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prealert`
--

DROP TABLE IF EXISTS `prealert`;
CREATE TABLE `prealert` (
  `ID_Prealert` bigint(255) NOT NULL,
  `ID_Envio_Prealert` varchar(255) DEFAULT NULL,
  `Origen` varchar(255) NOT NULL,
  `SiteName` varchar(255) NOT NULL,
  `Destino` varchar(255) DEFAULT NULL,
  `SiteName_Destino` varchar(255) DEFAULT NULL,
  `EmpresaTransporte` varchar(255) DEFAULT NULL,
  `Transportista` varchar(255) DEFAULT NULL,
  `Placas` varchar(255) DEFAULT NULL,
  `Orden` bigint(255) DEFAULT NULL,
  `Paquetera` varchar(255) DEFAULT NULL,
  `Marchamo` varchar(255) DEFAULT NULL,
  `Responsable` varchar(255) DEFAULT NULL,
  `Fecha` date DEFAULT NULL,
  `fecha_hora` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recibo_cc`
--

DROP TABLE IF EXISTS `recibo_cc`;
CREATE TABLE `recibo_cc` (
  `id_recibo_cc` bigint(20) DEFAULT NULL,
  `paquetera` varchar(255) NOT NULL,
  `Orden` bigint(20) NOT NULL,
  `accion` varchar(255) DEFAULT NULL,
  `Comentario` varchar(255) DEFAULT NULL,
  `facility` varchar(255) NOT NULL,
  `site` varchar(255) NOT NULL,
  `Responsable` varchar(255) NOT NULL,
  `fecha` date NOT NULL,
  `fecha_hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recibo_fc`
--

DROP TABLE IF EXISTS `recibo_fc`;
CREATE TABLE `recibo_fc` (
  `ID_Recibo` bigint(50) NOT NULL,
  `ID_Envio_Prealert` varchar(255) DEFAULT NULL,
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

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `ID` bigint(100) NOT NULL,
  `Nombre` varchar(250) NOT NULL,
  `Apellido` varchar(255) NOT NULL,
  `Usuario` varchar(70) NOT NULL,
  `ltrabajo` varchar(250) NOT NULL,
  `cdt` varchar(255) NOT NULL,
  `Rango` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`ID`, `Nombre`, `Apellido`, `Usuario`, `ltrabajo`, `cdt`, `Rango`) VALUES
(0, 'Administrador', '01', 'admin', 'Fulfillment', 'Odonnell', 'Administrador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salida_svcs`
--

DROP TABLE IF EXISTS `salida_svcs`;
CREATE TABLE `salida_svcs` (
  `ID_S_svcs` bigint(100) NOT NULL,
  `Centro_de_trabajo_donde_te_encuentras` varchar(255) NOT NULL,
  `Tarimas_enviadas` bigint(100) NOT NULL,
  `Gaylord_Enviados` bigint(100) NOT NULL,
  `Cross_Dock` varchar(250) NOT NULL,
  `Responsable` varchar(250) NOT NULL,
  `Fecha_Creación` date NOT NULL,
  `Fecha_Hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `entrada_svcs`
--
ALTER TABLE `entrada_svcs`
  ADD PRIMARY KEY (`ID_E_svcs`);

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
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `salida_svcs`
--
ALTER TABLE `salida_svcs`
  ADD PRIMARY KEY (`ID_S_svcs`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `entrada_svcs`
--
ALTER TABLE `entrada_svcs`
  MODIFY `ID_E_svcs` bigint(100) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ordenes_no_procesables`
--
ALTER TABLE `ordenes_no_procesables`
  MODIFY `id_orden` bigint(100) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `prealert`
--
ALTER TABLE `prealert`
  MODIFY `ID_Prealert` bigint(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recibo_fc`
--
ALTER TABLE `recibo_fc`
  MODIFY `ID_Recibo` bigint(50) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `ID` bigint(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- AUTO_INCREMENT de la tabla `salida_svcs`
--
ALTER TABLE `salida_svcs`
  MODIFY `ID_S_svcs` bigint(100) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
