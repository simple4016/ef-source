-- //ef-token
INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0x2f47BE95129c4bA94633A06f7C2e66488D7f8d49','18160ddd',NULL,'http://172.31.40.23:8580/heth/method/call',NULL,'2022-04-22 00:00:00','totalSupply',0,1,7);
-- vault
INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0xEa31426fd6f5194Edf9ee9097Db61b1Fb72EB890','e25aa5fa',NULL,'http://172.31.40.23:8580/heth/method/call',NULL,'2022-04-22 00:00:00','virtualPrice',0,1,6);

-- vault
INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0xEa31426fd6f5194Edf9ee9097Db61b1Fb72EB890','0x405007275853f6b040feb6bd41de0d355501031f20550aa7b4278f89ab83cf35','0xBACA74','http://172.31.40.23:8580/heth/transaction/call',NULL,'2022-04-22 00:00:00','Deposit',0,1,5);
-- vault
INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0xEa31426fd6f5194Edf9ee9097Db61b1Fb72EB890','0x63cb2c43362bdfc2f91eb3273ae0cf086faea513e1bf1faffa880c593e2e3d0f','0xBACA74','http://172.31.40.23:8580/heth/transaction/call',NULL,'2022-04-22 00:00:00','Withdraw',0,1,4);

--eth的不需要 -- vault
--INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
--VALUES ('0xEa31426fd6f5194Edf9ee9097Db61b1Fb72EB890','890fa413',NULL,NULL,NULL,'2022-04-22 00:00:00','feeRatio',0,1,3);

-- //ef-token  or controller
INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0x2f47BE95129c4bA94633A06f7C2e66488D7f8d49','313ce567',NULL,NULL,NULL,'2022-04-22 00:00:00','decimals',0,1,2);

--eth的不需要 -- vault
--INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
--VALUES ('0xEa31426fd6f5194Edf9ee9097Db61b1Fb72EB890','70f9e52f',NULL,NULL,NULL,'2022-04-22 00:00:00','fee',0,1,1);

-- usdc
-- 杠杆eth的因为程序里写的usdc_ration为usdc的换算关系，如果换成低风险的，需要把这个值订阅decimal相同的
INSERT INTO `subscribe` (`contract_address`,`topics`,`from_block`,`receive_address`,`filter_id`,`create_time`,`trade_type`,`is_del`,`status`,`order_init`)
VALUES ('0x2f47BE95129c4bA94633A06f7C2e66488D7f8d49','313ce567',NULL,NULL,NULL,'2022-04-22 00:00:00','usdc_ration',0,1,1);

-- 初始化程序的时候，会有is_profit置为0的情况
udpate transaction_record set is_profit = 1 where is_profit = 0;