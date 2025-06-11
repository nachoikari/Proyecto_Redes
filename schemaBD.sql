CREATE DATABASE  IF NOT EXISTS `RedesSinpe` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `RedesSinpe`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: RedesSinpe
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Usuario` (
  `idUsuario` int NOT NULL AUTO_INCREMENT,
  `usuario_cedula` varchar(45) NOT NULL,
  `usuario_password` varchar(45) NOT NULL,
  `usuario_nombre` varchar(45) DEFAULT NULL,
  `usuario_primer_apellido` varchar(45) DEFAULT NULL,
  `usuario_segundo_apellido` varchar(45) DEFAULT NULL,
  `usuario_numero` varchar(8) NOT NULL,
  `usuario_monto` float DEFAULT NULL,
  PRIMARY KEY (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
INSERT INTO `Usuario` VALUES (1,'601230456','clave123','Carlos','Mora','Jiménez','96123456',60673),(2,'701110222','mipass45','María','Fernández','Solano','96234567',121000),(3,'402222333','1234abcd','José','Ramírez','Acosta','96345678',47000.5),(4,'503334444','admin321','Laura','Campos','Gómez','96456789',130000),(5,'304445555','contra123','Andrés','Chaves','Monge','96567890',85000),(6,'205556666','qwerty78','Daniela','Pérez','Rojas','96678901',67500),(7,'106667777','abc12345','Luis','Vargas','Navarro','96789012',47000.8);
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_transacciones`
--

DROP TABLE IF EXISTS `log_transacciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_transacciones` (
  `id_transaccion` int NOT NULL AUTO_INCREMENT,
  `detalle` varchar(80) DEFAULT NULL,
  `numero_emisor` varchar(45) DEFAULT NULL,
  `numero_receptor` varchar(45) DEFAULT NULL,
  `id_cliente` int DEFAULT NULL,
  `fecha_transaccion` date DEFAULT NULL,
  `estado_transaccion` varchar(200) DEFAULT NULL,
  `monto` float DEFAULT NULL,
  PRIMARY KEY (`id_transaccion`),
  KEY `FK_ID_cliente_idx` (`id_cliente`),
  CONSTRAINT `FK_ID_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `Usuario` (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_transacciones`
--

LOCK TABLES `log_transacciones` WRITE;
/*!40000 ALTER TABLE `log_transacciones` DISABLE KEYS */;
INSERT INTO `log_transacciones` VALUES (1,'Prueba log','96123456','96234567',1,'2025-06-01','COMPLETADA: ENVÍO INTERNO',NULL),(2,'Prueba log','96123456','96234567',2,'2025-06-01','COMPLETADA: RECEPCIÓN INTERNA',NULL),(3,'Prueba log','96123456','96234567',2,'2025-06-01','COMPLETADA: RECEPCIÓN EXTERNA',NULL),(4,'Prueba xd 2','96123456','96234567',1,'2025-06-07','COMPLETADA: ENVÍO INTERNO',NULL),(5,'Prueba xd 2','96123456','96234567',2,'2025-06-07','COMPLETADA: RECEPCIÓN INTERNA',NULL),(6,'Tomela marco','96123456','77123456',1,'2025-06-09','COMPLETADA: EXITOSA',NULL),(7,'Tomela marco','96123456','77123456',1,'2025-06-09','ERROR: TRANSACCION RECHAZA',NULL),(8,'sapo','77123456','96123456',1,'2009-09-06','COMPLETADA: RECEPCIÓN EXTERNA',NULL),(9,'pago','88181736','96123456',1,'2025-06-09','COMPLETADA: RECEPCIÓN EXTERNA',NULL),(10,'SINPE a hector ','01888888','96123456',1,'2025-06-09','COMPLETADA: RECEPCIÓN EXTERNA',NULL),(11,'Tomela grego','96123456','01888888',1,'2025-06-09','COMPLETADA: EXITOSA',NULL),(12,'Tomela kim x2','96345678','88181736',3,'2025-06-09','COMPLETADA: EXITOSA',NULL),(13,'SINPE a hector ','01888888','96123456',1,'2025-06-09','COMPLETADA: RECEPCIÓN EXTERNA',NULL),(14,'Pago','13617819','96123456',1,'2025-06-09','COMPLETADA: RECEPCIÓN EXTERNA',NULL),(15,'Tomela jhashua','96345678','77123456',3,'2025-06-09','COMPLETADA: EXITOSA',NULL),(16,'sapo','77123456','96123456',1,'2025-06-09','COMPLETADA: RECEPCIÓN EXTERNA',NULL),(17,'Pruebas locacles xd','96123456','96234567',1,'2025-06-10','COMPLETADA: ENVÍO INTERNO',NULL),(18,'Pruebas locacles xd','96123456','96234567',2,'2025-06-10','COMPLETADA: RECEPCIÓN INTERNA',NULL),(19,'Pruebas locales xd x10','96123456','96234567',1,'2025-06-10','COMPLETADA: ENVÍO INTERNO',NULL),(20,'Pruebas locales xd x10','96123456','96234567',2,'2025-06-10','COMPLETADA: RECEPCIÓN INTERNA',NULL),(26,'sinpe a andres pura vida','96123456','96567890',1,'2025-06-10','COMPLETADA: ENVÍO INTERNO',1000),(27,'sinpe a andres pura vida','96123456','96567890',5,'2025-06-10','COMPLETADA: EXITOSA',1000),(28,'Conocedora daniela','96567890','96678901',5,'2025-06-10','COMPLETADA: ENVÍO INTERNO',5000),(29,'Conocedora daniela','96567890','96678901',6,'2025-06-10','COMPLETADA: EXITOSA',5000);
/*!40000 ALTER TABLE `log_transacciones` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-10 22:09:21
