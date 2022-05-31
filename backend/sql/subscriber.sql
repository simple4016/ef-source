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


INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0x2f47BE95129c4bA94633A06f7C2e66488D7f8d49','18160ddd',NULL,'http://172.31.40.23:8580/heth/method/call',NULL,'2022-04-22 00:00:00','totalSupply',0,1,7);

INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0xEa31426fd6f5194Edf9ee9097Db61b1Fb72EB890','e25aa5fa',NULL,'http://172.31.40.23:8580/heth/method/call',NULL,'2022-04-22 00:00:00','virtualPrice',0,1,6);

INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0xEa31426fd6f5194Edf9ee9097Db61b1Fb72EB890','0x405007275853f6b040feb6bd41de0d355501031f20550aa7b4278f89ab83cf35','0xBACA74','http://172.31.40.23:8580/heth/transaction/call',NULL,'2022-04-22 00:00:00','Deposit',0,1,5);

INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0xEa31426fd6f5194Edf9ee9097Db61b1Fb72EB890','0x63cb2c43362bdfc2f91eb3273ae0cf086faea513e1bf1faffa880c593e2e3d0f','0xBACA74','http://172.31.40.23:8580/heth/transaction/call',NULL,'2022-04-22 00:00:00','Withdraw',0,1,4);

--eth的不需要
--INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
--VALUES ('0xEa31426fd6f5194Edf9ee9097Db61b1Fb72EB890','890fa413',NULL,NULL,NULL,'2022-04-22 00:00:00','feeRatio',0,1,3);

INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0x2f47BE95129c4bA94633A06f7C2e66488D7f8d49','313ce567',NULL,NULL,NULL,'2022-04-22 00:00:00','decimals',0,1,2);

--eth的不需要
--INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
--VALUES ('0xEa31426fd6f5194Edf9ee9097Db61b1Fb72EB890','70f9e52f',NULL,NULL,NULL,'2022-04-22 00:00:00','fee',0,1,1);

-- 杠杆eth的因为程序里写的usdc_ration为usdc的换算关系，如果换成低风险的，需要把这个值订阅decimal相同的
INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0x2f47BE95129c4bA94633A06f7C2e66488D7f8d49','313ce567',NULL,NULL,NULL,'2022-04-22 00:00:00','usdc_ration',0,1,1);

-- 初始化程序的时候，会有is_profit置为0的情况
udpate transaction_record set is_profit = 1 where is_profit = 0;