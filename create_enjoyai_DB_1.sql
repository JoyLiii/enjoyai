CREATE DATABASE  IF NOT EXISTS `automl_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE DATABASE  IF NOT EXISTS `automl_file_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE DATABASE  IF NOT EXISTS `automl_file_detail_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE DATABASE  IF NOT EXISTS `automl_rule_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE DATABASE  IF NOT EXISTS `automl_testing_result_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;



USE `automl_db`;
-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: automl_db
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `association_rule_list`
--

DROP TABLE IF EXISTS `association_rule_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `association_rule_list` (
  `association_rule_id` varchar(45) NOT NULL,
  `association_rule_name` varchar(256) DEFAULT NULL,
  `database_number` varchar(45) DEFAULT NULL,
  `database_name` varchar(256) DEFAULT NULL,
  `target` varchar(256) DEFAULT NULL,
  `class_label_str` varchar(256) DEFAULT NULL,
  `association_rule_key_feature` text,
  `association_rule_cluster` json DEFAULT NULL,
  `association_rule_plot` text,
  `association_rule_status` varchar(45) DEFAULT NULL,
  `association_rule_time` datetime DEFAULT NULL,
  `association_rule_runtime` datetime DEFAULT NULL,
  `dept` varchar(45) DEFAULT NULL,
  `creator` varchar(45) DEFAULT NULL,
  `creator_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`association_rule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL DEFAULT '0',
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `dept` varchar(150) DEFAULT '',
  `is_staff` tinyint(1) NOT NULL DEFAULT '1',
  `is_active` tinyint(1) NOT NULL DEFAULT '0',
  `date_joined` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `databse_info2`
--

DROP TABLE IF EXISTS `databse_info2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `databse_info2` (
  `Dataset_number` varchar(256) NOT NULL,
  `Dataset_name` varchar(256) DEFAULT NULL,
  `dept` varchar(50) DEFAULT NULL,
  `creator` varchar(50) DEFAULT NULL,
  `creator_id` varchar(50) DEFAULT NULL,
  `Target` varchar(256) DEFAULT NULL,
  `Row_no` int DEFAULT NULL,
  `Column_no` int DEFAULT NULL,
  `Column_list` text,
  `Type_list` text,
  `Logi_column_list` text,
  `Logi_type_list` text,
  `Dataset_status` varchar(256) DEFAULT NULL,
  `Dataset_path` varchar(256) DEFAULT NULL,
  `Dataset_size` varchar(45) DEFAULT NULL,
  `Upload_time` datetime DEFAULT NULL,
  `Modify_time` datetime DEFAULT NULL,
  `Heatmap_svg` longtext,
  `Profile_json` varchar(256) DEFAULT NULL,
  `Low_variance_columns` text,
  `Variable_distribution_plot` json DEFAULT NULL,
  `Skew_histogram_png` json DEFAULT NULL,
  `Heatmap_plot` json DEFAULT NULL,
  `N_variables` varchar(45) DEFAULT NULL,
  `N_observations` varchar(45) DEFAULT NULL,
  `N_miss` varchar(45) DEFAULT NULL,
  `N_duplicate` varchar(45) DEFAULT NULL,
  `N_datatime` varchar(45) DEFAULT NULL,
  `N_numeric` varchar(45) DEFAULT NULL,
  `N_category` varchar(45) DEFAULT NULL,
  KEY `index_name` (`Dataset_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `model_list`
--

DROP TABLE IF EXISTS `model_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `model_list` (
  `model_number` varchar(100) NOT NULL,
  `model_name` varchar(256) DEFAULT NULL,
  `train_dataset` varchar(45) DEFAULT NULL,
  `test_dataset` varchar(45) DEFAULT NULL,
  `target_column` varchar(45) DEFAULT NULL,
  `model_info` varchar(45) DEFAULT NULL,
  `scorer` varchar(45) DEFAULT NULL,
  `model_score` varchar(45) DEFAULT NULL,
  `test_score` varchar(45) DEFAULT NULL,
  `dept` varchar(45) DEFAULT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  `parameter_json` longtext,
  `parameter_json_spe` json DEFAULT NULL,
  `binary_multi_classify` varchar(45) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `compare_model_json` json DEFAULT NULL,
  `plotly_json` longtext,
  `error_logs` longtext,
  PRIMARY KEY (`model_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `para_recommend_list`
--

DROP TABLE IF EXISTS `para_recommend_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `para_recommend_list` (
  `recommend_id` varchar(45) NOT NULL,
  `recommend_name` varchar(256) DEFAULT NULL,
  `database_number` varchar(45) DEFAULT NULL,
  `database_name` varchar(256) DEFAULT NULL,
  `target` varchar(256) DEFAULT NULL,
  `class_label_str` varchar(256) DEFAULT NULL,
  `feature_list_json` longblob,
  `better_LS` varchar(45) DEFAULT NULL,
  `recommend_result` longtext,
  `recommend_plot` json DEFAULT NULL,
  `recommend_status` varchar(45) DEFAULT NULL,
  `recommend_time` datetime DEFAULT NULL,
  `recommend_runtime` datetime DEFAULT NULL,
  `dept` varchar(45) DEFAULT NULL,
  `creator` varchar(45) DEFAULT NULL,
  `creator_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`recommend_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shap_list`
--

DROP TABLE IF EXISTS `shap_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shap_list` (
  `shap_id` varchar(45) NOT NULL,
  `experiment_number` varchar(45) DEFAULT NULL,
  `experiment_name` varchar(256) DEFAULT NULL,
  `model_name` varchar(256) DEFAULT NULL,
  `testing_data` varchar(256) DEFAULT NULL,
  `n_fold` varchar(45) DEFAULT NULL,
  `training_feature_list` json DEFAULT NULL,
  `feature_set` varchar(45) DEFAULT NULL,
  `summary_plot` json DEFAULT NULL,
  `correlation_plot` json DEFAULT NULL,
  `reason_plot` json DEFAULT NULL,
  `pdp_plot` json DEFAULT NULL,
  `msa_plot` json DEFAULT NULL,
  `pfi_plot` json DEFAULT NULL,
  `plot_status` varchar(45) DEFAULT NULL,
  `shap_runtime` datetime DEFAULT NULL,
  PRIMARY KEY (`shap_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `testing_model_list`
--

DROP TABLE IF EXISTS `testing_model_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `testing_model_list` (
  `testing_id` varchar(45) DEFAULT NULL,
  `testing_name` varchar(45) DEFAULT NULL,
  `experiment_number` varchar(45) DEFAULT NULL,
  `experiment_name` varchar(256) DEFAULT NULL,
  `model_name` varchar(256) DEFAULT NULL,
  `testing_data_path` varchar(256) DEFAULT NULL,
  `parameter_json` json DEFAULT NULL,
  `testing_result_json` json DEFAULT NULL,
  `dept` varchar(45) DEFAULT NULL,
  `user_id` varchar(45) DEFAULT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  `testing_status` varchar(45) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transformed_dataset_info`
--

DROP TABLE IF EXISTS `transformed_dataset_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transformed_dataset_info` (
  `transformed_dataset_number` varchar(100) NOT NULL,
  `transformed_dataset_name` varchar(256) DEFAULT NULL,
  `used_dataset_number` varchar(100) DEFAULT NULL,
  `parameter_json` json DEFAULT NULL,
  `dept` varchar(45) DEFAULT NULL,
  `creator` varchar(45) DEFAULT NULL,
  `creator_id` varchar(45) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `transformed_dataset_status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`transformed_dataset_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-01 15:01:58
