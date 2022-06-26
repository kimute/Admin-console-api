-- test用　table for sp console
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    userId VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role INT NOT NULL,
    created_at,timestamp,
    updated_at,timestamp
    PRIMARY KEY (id)
);

--  DB for aws congnito
CREATE TABLE `cognito` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_pool_id` varchar(255) NOT NULL COMMENT 'user id',
  `email` varchar(255) DEFAULT NULL COMMENT 'email',
  `preferred_username` varchar(255) DEFAULT NULL COMMENT 'user name',
  `role_name` varchar(255) NOT NULL COMMENT 'role',
  `last_login_at` timestamp NULL DEFAULT NULL COMMENT 'lastlogin',
  `verify_code` varchar(255) DEFAULT NULL COMMENT 'authentication code',
  `verify_mail` varchar(255) DEFAULT NULL COMMENT 'authentication mail',
  `verify_expiration` timestamp NULL DEFAULT NULL COMMENT 'confirmation expiration date',
  `status` varchar(2) DEFAULT NULL COMMENT 'status',
  `company_code` varchar(13) DEFAULT NULL COMMENT 'company code\n\n',
  `user_code` varchar(13) DEFAULT NULL COMMENT 'user code',
  `insert_id` bigint(20) DEFAULT NULL COMMENT 'registered person',
  `insert_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Registration date and time',
  `update_id` bigint(20) DEFAULT NULL COMMENT 'update person',
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Update Date and Time',
  `delete_id` bigint(20) DEFAULT NULL COMMENT '',
  `delete_at` timestamp NULL DEFAULT NULL COMMENT '',
  `delete_flag` int(1) DEFAULT '0' COMMENT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `cognito_unique1` (`user_pool_id`,`email`,`preferred_username`)
) ENGINE=InnoDB AUTO_INCREMENT=1160 DEFAULT CHARSET=utf8 COMMENT='cognito';


--  company table
CREATE TABLE `company` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '',
  `company_code` varchar(13) NOT NULL COMMENT '',
  `owner_staff_code` varchar(13) DEFAULT NULL COMMENT '',
  `company_name` varchar(255) NOT NULL COMMENT '',
  `company_representative` varchar(255) NOT NULL COMMENT '',
  `display_name`varchar(255) NOT NULL COMMENT '',
  `zip_code` varchar(255) DEFAULT NULL COMMENT '',
  `prefectures_code` varchar(13) DEFAULT NULL COMMENT '',
  `address1` varchar(255) DEFAULT NULL COMMENT '',
  `address2` varchar(255) DEFAULT NULL COMMENT '',
  `address3` varchar(255) DEFAULT NULL COMMENT '',
  `phone_number` varchar(255) NOT NULL COMMENT '',
  `email` varchar(255) NOT NULL COMMENT '',
  `department` varchar(255) DEFAULT NULL COMMENT '',
  `person_in_charge` varchar(255) DEFAULT NULL COMMENT '',
  `fax` varchar(255) DEFAULT NULL COMMENT 'FAX',
  `employee_count` int(11) DEFAULT NULL COMMENT '',
  `shop_count` int(11) DEFAULT NULL COMMENT '',
  `first_month_of_the_year` int(11) DEFAULT NULL COMMENT '',
  `privacy_policy_type` varchar(1) DEFAULT NULL COMMENT ''
  `privacy_policy_content` text DEFAULT NULL COMMENT ''
  `company_reservation_url` varchar(255) DEFAULT NULL COMMENT ''
  `insert_id` bigint(20) NOT NULL COMMENT 'registered person',
  `insert_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `update_id` bigint(20) NOT NULL COMMENT 'update person',
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Update Date and Time',
  `delete_id` bigint(20) DEFAULT NULL COMMENT '',
  `delete_at` timestamp NULL DEFAULT NULL COMMENT '',
  `delete_flag` int(1) NOT NULL DEFAULT '0' COMMENT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `company_index` (`company_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='company master';

 
CREATE TABLE `sp_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'company masterID',
  `company_code` varchar(13) NOT NULL COMMENT 'company code',
  `company_name` varchar(255) NOT NULL COMMENT '',
  `OEM` varchar(255) DEFAULT NULL COMMENT 'oem name',
  `sp_url` varchar(255) DEFAULT NULL COMMENT '',
  `insert_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `update_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Update Date and Time',
  `delete_at` timestamp NULL DEFAULT NULL COMMENT '',
  `delete_flag` int(1) NOT NULL DEFAULT '0' COMMENT 'delete flag',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `company_index` (`company_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='SP company master';