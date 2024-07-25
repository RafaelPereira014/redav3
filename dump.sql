-- MySQL dump 10.13  Distrib 8.2.0, for macos13.5 (x86_64)
--
-- Host: localhost    Database: redav4
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping routines for database 'redav4'
--
/*!50003 DROP PROCEDURE IF EXISTS `DeleteResourceAndScripts` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `DeleteResourceAndScripts`(
    IN p_resource_id INT
)
BEGIN
    -- Delete from Scripts table
    DELETE FROM Scripts WHERE resource_id = p_resource_id;
    
    -- Delete from Resources table
    DELETE FROM Resources WHERE id = p_resource_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetApprovedApps` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GetApprovedApps`(IN page INT, IN apps_per_page INT)
BEGIN
    DECLARE offset INT;
    SET offset = (page - 1) * apps_per_page;
    
    SELECT * FROM ApprovedApps
    LIMIT apps_per_page OFFSET offset;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `InsertResource` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `InsertResource`(
    IN p_title VARCHAR(255),
    IN p_slug VARCHAR(255),
    IN p_description TEXT,
    IN p_operation VARCHAR(255),
    IN p_operation_author VARCHAR(255),
    IN p_techResources TEXT,
    IN p_email VARCHAR(255),
    IN p_organization VARCHAR(255),
    IN p_duration VARCHAR(255),
    IN p_highlight TINYINT,
    IN p_exclusive TINYINT,
    IN p_embed TEXT,
    IN p_link VARCHAR(255),
    IN p_author VARCHAR(255),
    IN p_approved TINYINT,
    IN p_approvedScientific TINYINT,
    IN p_approvedLinguistic TINYINT,
    IN p_status TINYINT,
    IN p_accepted_terms TINYINT,
    IN p_created_at DATETIME,
    IN p_updated_at DATETIME,
    IN p_deleted_at DATETIME,
    IN p_user_id INT,
    IN p_type_id INT,
    IN p_image_id INT,
    IN p_hidden TINYINT
)
BEGIN
    -- Insert into Resources table
    INSERT INTO Resources (
        title, slug, description, operation, operation_author, techResources, email, organization, 
        duration, highlight, exclusive, embed, link, author, approved, approvedScientific, approvedLinguistic, 
        status, accepted_terms, created_at, updated_at, deleted_at, user_id, type_id, image_id, hidden
    )
    VALUES (
        p_title, p_slug, p_description, p_operation, p_operation_author, p_techResources, p_email, p_organization, 
        p_duration, p_highlight, p_exclusive, p_embed, p_link, p_author, p_approved, p_approvedScientific, p_approvedLinguistic, 
        p_status, p_accepted_terms, p_created_at, p_updated_at, p_deleted_at, p_user_id, p_type_id, p_image_id, p_hidden
    );

    -- Return the last inserted ID
    SELECT LAST_INSERT_ID() AS resource_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `InsertTaxonomyDetails` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `InsertTaxonomyDetails`(
    IN p_resource_id INT,
    IN p_idiomas_title VARCHAR(255),
    IN p_formato_title VARCHAR(255),
    IN p_modo_utilizacao_title VARCHAR(255),
    IN p_requisitos_tecnicos_title VARCHAR(255),
    IN p_anos_escolaridade_title VARCHAR(255)
)
BEGIN
    DECLARE v_taxonomy_id INT;
    DECLARE v_term_id INT;

    -- Insert into Terms and associate with resource
    -- Idiomas
    SELECT id INTO v_taxonomy_id FROM Taxonomies WHERE title = 'Idiomas';
    INSERT INTO Terms (title, taxonomy_id, created_at, updated_at)
    VALUES (p_idiomas_title, v_taxonomy_id, NOW(), NOW());
    SET v_term_id = LAST_INSERT_ID();
    INSERT INTO resource_terms (resource_id, term_id, created_at, updated_at)
    VALUES (p_resource_id, v_term_id, NOW(), NOW());

    -- Formato
    SELECT id INTO v_taxonomy_id FROM Taxonomies WHERE title = 'Formato';
    INSERT INTO Terms (title, taxonomy_id, created_at, updated_at)
    VALUES (p_formato_title, v_taxonomy_id, NOW(), NOW());
    SET v_term_id = LAST_INSERT_ID();
    INSERT INTO resource_terms (resource_id, term_id, created_at, updated_at)
    VALUES (p_resource_id, v_term_id, NOW(), NOW());

    -- Modos de utilização
    SELECT id INTO v_taxonomy_id FROM Taxonomies WHERE title = 'Modos de utilização';
    INSERT INTO Terms (title, taxonomy_id, created_at, updated_at)
    VALUES (p_modo_utilizacao_title, v_taxonomy_id, NOW(), NOW());
    SET v_term_id = LAST_INSERT_ID();
    INSERT INTO resource_terms (resource_id, term_id, created_at, updated_at)
    VALUES (p_resource_id, v_term_id, NOW(), NOW());

    -- Requisitos Técnicos
    SELECT id INTO v_taxonomy_id FROM Taxonomies WHERE title = 'Requisitos Técnicos';
    INSERT INTO Terms (title, taxonomy_id, created_at, updated_at)
    VALUES (p_requisitos_tecnicos_title, v_taxonomy_id, NOW(), NOW());
    SET v_term_id = LAST_INSERT_ID();
    INSERT INTO resource_terms (resource_id, term_id, created_at, updated_at)
    VALUES (p_resource_id, v_term_id, NOW(), NOW());

    -- Anos de escolaridade
    SELECT id INTO v_taxonomy_id FROM Taxonomies WHERE title = 'Anos de escolaridade';
    INSERT INTO Terms (title, taxonomy_id, created_at, updated_at)
    VALUES (p_anos_escolaridade_title, v_taxonomy_id, NOW(), NOW());
    SET v_term_id = LAST_INSERT_ID();
    INSERT INTO resource_terms (resource_id, term_id, created_at, updated_at)
    VALUES (p_resource_id, v_term_id, NOW(), NOW());
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateResourceDetails` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateResourceDetails`(
    IN p_resource_id INT,
    IN p_title VARCHAR(255),
    IN p_slug VARCHAR(255),
    IN p_description TEXT,
    IN p_operation VARCHAR(50),
    IN p_operation_author VARCHAR(255),
    IN p_organization VARCHAR(255),
    IN p_link VARCHAR(255),
    IN p_author VARCHAR(255),
    IN p_updated_at DATETIME,
    IN p_user_id INT,
    IN p_type_id INT,
    IN p_image_id INT,
    IN p_hidden TINYINT
)
BEGIN
    UPDATE Resources SET
        title = p_title,
        slug = p_slug,
        description = p_description,
        operation = p_operation,
        operation_author = p_operation_author,
        organization = p_organization,
        link = p_link,
        author = p_author,
        updated_at = p_updated_at,
        user_id = p_user_id,
        type_id = p_type_id,
        image_id = p_image_id,
        hidden = p_hidden
    WHERE id = p_resource_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `UpdateTaxonomyDetails` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateTaxonomyDetails`(
    IN p_resource_id INT,
    IN p_idiomas_selected JSON,
    IN p_formatos_selected JSON,
    IN p_use_mode_selected JSON,
    IN p_requirements_selected JSON
)
BEGIN
    DECLARE v_term_id INT;
    DECLARE v_taxonomy_id INT;
    DECLARE v_term_title VARCHAR(255);
    
    -- Define taxonomy IDs
    DECLARE v_idiomas_taxonomy_id INT DEFAULT 12;
    DECLARE v_formato_taxonomy_id INT DEFAULT 11;
    DECLARE v_modos_utilizacao_taxonomy_id INT DEFAULT 10;
    DECLARE v_requisitos_tecnicos_taxonomy_id INT DEFAULT 13;

    -- Delete existing term associations for the resource
    DELETE FROM resource_terms WHERE resource_id = p_resource_id;

    -- Helper function to get term ID for a title and taxonomy ID
    SET @term_id_query = "SELECT id FROM Terms WHERE title = ? AND taxonomy_id = ? LIMIT 1";

    -- Iterate over idiomas_selected
    SET @terms = p_idiomas_selected;
    WHILE JSON_LENGTH(@terms) > 0 DO
        SET v_term_title = JSON_UNQUOTE(JSON_EXTRACT(@terms, '$[0]'));
        SET @terms = JSON_REMOVE(@terms, '$[0]');
        
        PREPARE stmt FROM @term_id_query;
        SET @title = v_term_title;
        SET @taxonomy_id = v_idiomas_taxonomy_id;
        EXECUTE stmt USING @title, @taxonomy_id;
        DEALLOCATE PREPARE stmt;
        
        IF v_term_id IS NOT NULL THEN
            INSERT INTO resource_terms (resource_id, term_id, created_at, updated_at)
            VALUES (p_resource_id, v_term_id, NOW(), NOW());
        END IF;
    END WHILE;

    -- Iterate over formatos_selected
    SET @terms = p_formatos_selected;
    WHILE JSON_LENGTH(@terms) > 0 DO
        SET v_term_title = JSON_UNQUOTE(JSON_EXTRACT(@terms, '$[0]'));
        SET @terms = JSON_REMOVE(@terms, '$[0]');
        
        PREPARE stmt FROM @term_id_query;
        SET @title = v_term_title;
        SET @taxonomy_id = v_formato_taxonomy_id;
        EXECUTE stmt USING @title, @taxonomy_id;
        DEALLOCATE PREPARE stmt;
        
        IF v_term_id IS NOT NULL THEN
            INSERT INTO resource_terms (resource_id, term_id, created_at, updated_at)
            VALUES (p_resource_id, v_term_id, NOW(), NOW());
        END IF;
    END WHILE;

    -- Iterate over use_mode_selected
    SET @terms = p_use_mode_selected;
    WHILE JSON_LENGTH(@terms) > 0 DO
        SET v_term_title = JSON_UNQUOTE(JSON_EXTRACT(@terms, '$[0]'));
        SET @terms = JSON_REMOVE(@terms, '$[0]');
        
        PREPARE stmt FROM @term_id_query;
        SET @title = v_term_title;
        SET @taxonomy_id = v_modos_utilizacao_taxonomy_id;
        EXECUTE stmt USING @title, @taxonomy_id;
        DEALLOCATE PREPARE stmt;
        
        IF v_term_id IS NOT NULL THEN
            INSERT INTO resource_terms (resource_id, term_id, created_at, updated_at)
            VALUES (p_resource_id, v_term_id, NOW(), NOW());
        END IF;
    END WHILE;

    -- Iterate over requirements_selected
    SET @terms = p_requirements_selected;
    WHILE JSON_LENGTH(@terms) > 0 DO
        SET v_term_title = JSON_UNQUOTE(JSON_EXTRACT(@terms, '$[0]'));
        SET @terms = JSON_REMOVE(@terms, '$[0]');
        
        PREPARE stmt FROM @term_id_query;
        SET @title = v_term_title;
        SET @taxonomy_id = v_requisitos_tecnicos_taxonomy_id;
        EXECUTE stmt USING @title, @taxonomy_id;
        DEALLOCATE PREPARE stmt;
        
        IF v_term_id IS NOT NULL THEN
            INSERT INTO resource_terms (resource_id, term_id, created_at, updated_at)
            VALUES (p_resource_id, v_term_id, NOW(), NOW());
        END IF;
    END WHILE;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-25 16:43:28
