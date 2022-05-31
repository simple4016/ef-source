
INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0xE6e0Ab5e9352202E99415bc0Cb9a08a5072d7596','18160ddd',NULL,'http://10.10.10.72:8380/mheth/method/call',NULL,'2022-04-22 00:00:00','totalSupply',0,1,7);

INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0x9fd5F2E7102d90e29ddb9A079853658e85cB03fa','e25aa5fa',NULL,'http://10.10.10.72:8380/mheth/method/call',NULL,'2022-04-22 00:00:00','virtualPrice',0,1,6);


INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0x9fd5F2E7102d90e29ddb9A079853658e85cB03fa','0x405007275853f6b040feb6bd41de0d355501031f20550aa7b4278f89ab83cf35','0xE25AAC','http://10.10.10.72:8380/mheth/transaction/call',NULL,'2022-04-22 00:00:00','Deposit',0,1,5);

INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0x9fd5F2E7102d90e29ddb9A079853658e85cB03fa','0xbdd509a6ec35e0e438c8b76b0ccbd5cac5d64387affc672f95bdcb361c817a22','0xE25AAC','http://10.10.10.72:8380/mheth/transaction/call',NULL,'2022-04-22 00:00:00','Withdraw',0,1,4);


INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0xE6e0Ab5e9352202E99415bc0Cb9a08a5072d7596','313ce567',NULL,NULL,NULL,'2022-04-22 00:00:00','decimals',0,1,2);

INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0xE6e0Ab5e9352202E99415bc0Cb9a08a5072d7596','313ce567',NULL,NULL,NULL,'2022-04-22 00:00:00','usdc_ration',0,1,1);
