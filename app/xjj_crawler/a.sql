

create table `detail_info` (
	`id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`url` varchar(300) NOT NULL,
	`isGet` int(11) NOT NULL DEFAULT 0,
	`title` varchar(180) DEFAULT NULL,
	`style` varchar(30) DEFAULT NULL,
	`district` varchar(60) DEFAULT NULL,
	`detailAddr` varchar(360) DEFAULT NULL,
	`source` varchar(180) DEFAULT NULL,
	`amount` varchar(48) DEFAULT NULL,
	`age` varchar(48) DEFAULT NULL,
	`leveldesc` varchar(150) DEFAULT NULL,
	`appear` varchar(240) DEFAULT NULL,
	`service` varchar(240) DEFAULT NULL,
	`price` varchar(360) DEFAULT NULL,
	`timeopen` varchar(150) DEFAULT NULL,
	`environ` varchar(180) DEFAULT NULL,
	`safe` varchar(90) DEFAULT NULL,
	`judge` varchar(90) DEFAULT NULL,
	`contact` blob  DEFAULT NULL,
	`detail` text 
); 
