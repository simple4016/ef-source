CREATE TABLE `supply` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `total_supply` varchar(100) DEFAULT NULL COMMENT 'total_supply',
  `virtual_price` varchar(100) DEFAULT NULL COMMENT 'virtual_price',
  `crv` varchar(100) DEFAULT NULL COMMENT 'crv',
  `date_time` varchar(64) DEFAULT NULL COMMENT 'date_time',
  `apy` varchar(100) DEFAULT NULL COMMENT 'apy',
  `gas` varchar(100) DEFAULT NULL,
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'create_date',
  `average_days` int(11) DEFAULT '7' COMMENT 'average_days',
  PRIMARY KEY (`id`),
  UNIQUE KEY `date_time_UNIQUE` (`date_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='supply';



CREATE TABLE `subscribe` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `contract_address` varchar(64) DEFAULT NULL COMMENT 'contract address',
  `topics` varchar(500) DEFAULT NULL COMMENT 'topics',
  `from_block` varchar(64) DEFAULT NULL COMMENT 'from_block',
  `receive_address` varchar(64) DEFAULT NULL COMMENT 'receive_address',
  `filter_id` varchar(64) DEFAULT NULL COMMENT 'filter_id',
  `create_time` datetime DEFAULT NULL COMMENT 'create_time',
  `trade_type` varchar(45) DEFAULT NULL,
  `is_del` int(11) DEFAULT '0',
  `status` int(11) DEFAULT '0',
  `order_init` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='subscribe';



CREATE TABLE `transaction_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `user_address` varchar(64) DEFAULT NULL COMMENT 'user_address',
  `transaction_hash` varchar(500) DEFAULT NULL COMMENT 'transaction_hash',
  `cff_amount` varchar(100) DEFAULT NULL COMMENT 'cff_amount',
  `virtual_price` varchar(100) DEFAULT NULL COMMENT 'virtual_price',
  `target_fee` varchar(100) DEFAULT NULL COMMENT 'target_fee',
  `trade_type` varchar(16) DEFAULT NULL COMMENT 'trade_type_withdraw/deposit',
  `trade_time` varchar(64) DEFAULT NULL COMMENT 'trade_time',
  `sub_id` int(11) DEFAULT NULL,
  `stable_amount` varchar(100) DEFAULT NULL,
  `target_amount` varchar(100) DEFAULT NULL,
  `is_profit` int(11) DEFAULT '1' COMMENT '1-profit 0-nonprofit',
  PRIMARY KEY (`id`),
  UNIQUE KEY `transaction_hash_UNIQUE` (`transaction_hash`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='transaction_record';