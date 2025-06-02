-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: RedesSinpe
-- ------------------------------------------------------
-- Server version	8.0.42

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
INSERT INTO `Usuario` VALUES (1,'601230456','clave123','Carlos','Mora','Jiménez','96123456',79000),(2,'701110222','mipass45','María','Fernández','Solano','96234567',106000),(3,'402222333','1234abcd','José','Ramírez','Acosta','96345678',52000.5),(4,'503334444','admin321','Laura','Campos','Gómez','96456789',130000),(5,'304445555','contra123','Andrés','Chaves','Monge','96567890',89000),(6,'205556666','qwerty78','Daniela','Pérez','Rojas','96678901',62500),(7,'106667777','abc12345','Luis','Vargas','Navarro','96789012',47000.8);
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
  PRIMARY KEY (`id_transaccion`),
  KEY `FK_ID_cliente_idx` (`id_cliente`),
  CONSTRAINT `FK_ID_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `Usuario` (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_transacciones`
--

LOCK TABLES `log_transacciones` WRITE;
/*!40000 ALTER TABLE `log_transacciones` DISABLE KEYS */;
INSERT INTO `log_transacciones` VALUES (1,'Prueba log','96123456','96234567',1,'2025-06-01','COMPLETADA: ENVÍO INTERNO'),(2,'Prueba log','96123456','96234567',2,'2025-06-01','COMPLETADA: RECEPCIÓN INTERNA'),(3,'Prueba log','96123456','96234567',2,'2025-06-01','COMPLETADA: RECEPCIÓN EXTERNA');
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

-- Dump completed on 2025-06-01 19:27:04
