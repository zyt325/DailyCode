# 部署
## apache   127.0.0.1:8002

note-8002.conf
```
Listen 8000
LoadModule wsgi_module "/var/opt/django/lib/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so"
WSGIPythonHome /var/opt/django
WSGIPythonPath /opt/django/notes

<VirtualHost *:8000>
    DocumentRoot /opt/django/notes/
    
    WSGIScriptAlias / /opt/django/notes/notes/wsgi.py
    <Directory /opt/django/notes/notes>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    ErrorLog "logs/tools-error.log"
    CustomLog "logs/tools-access.log" combined
</VirtualHost>
```

## nginx :80

note.conf
```
[root@vps4 conf.d]# cat /etc/nginx/conf.d/note.conf 
server {
	server_name  note.personer.tech;

	location / {
		proxy_pass http://127.0.0.1:8002;
		#proxy_set_header Host $host:$server_port;
		 client_max_body_size  100M;
	}
	location /static/ {
		root /opt/django/notes/;
		#autoindex on;
	}
	location /media/ {
		root /opt/django/notes/;
		#autoindex on;
	}
	location /uploads/ {
		root /opt/django/notes/media/;
		#autoindex on;
	}
	error_page 404 /404.html;
	    location = /404.html {
	}
	error_page 500 502 503 504 /50x.html;
	    location = /50x.html {
	}
}
```

# 数据库
## note mysql sql
- 表article中字段body是mediumblob

```
CREATE DATABASE /*!32312 IF NOT EXISTS*/`notes` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `notes`;

CREATE TABLE `zyt_articles` (
    `id` int(20) NOT NULL AUTO_INCREMENT,
    `title` varchar(50) NOT NULL,
    `body` mediumblob,
    `file_name` varchar(25) NOT NULL,
    `create_at` datetime NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `title` (`title`),
    UNIQUE KEY `file_name` (`file_name`)
   ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4

CREATE TABLE `zyt_articleClass` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `class_name` varchar(50) NOT NULL,
    `class_level` int(4) NOT NULL,
    PRIMARY KEY (`id`)
   ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4

CREATE TABLE `notes`.`zyt_users` ( 
    `id` INT(20) NOT NULL AUTO_INCREMENT , 
    `username` VARCHAR(20) NOT NULL , 
    `password` VARCHAR(200) NOT NULL , 
    `update_time` TIMESTAMP NOT NULL , PRIMARY KEY (`id`)
    ) ENGINE = InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
```

```
USE `notes`;
CREATE VIEW `note_article_view` 
AS (select `a`.`id` AS `article_id`,`a`.`body` AS `body`,`a`.`class_id` AS `class_id`,
`a`.`file_name` AS `file_name`,`a`.`title` AS `article_name`,`c`.`class_name` AS `class_name`, `c`.`upper_class` AS `upper_class` 
from (`note_article` `a` left join `note_class` `c` on((`a`.`class_id` = `c`.`id`))))
```

```
CREATE TABLE `zyt_articles_bak` (
    `id` int(20) NOT NULL AUTO_INCREMENT,
    `title` varchar(50) NOT NULL,
    `body` mediumblob,
    `file_name` varchar(25) NOT NULL,
    `create_at` datetime NOT NULL,
    PRIMARY KEY (`id`),
   ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4


CREATE DEFINER=`root`@`localhost` TRIGGER `articles_bak` BEFORE DELETE ON `zyt_articles` FOR EACH ROW 
INSERT INTO zyt_articles_bak(id,title,body,file_name,create_at) VALUE(old.id,old.title,old.body,old.file_name,old.create_at)
```

## tool mysql sql
`CREATE DATABASE `tools` /*!40100 DEFAULT CHARACTER SET utf8mb4 */`

```
CREATE TABLE `tools_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `desc` longtext,
  `type` int(11) NOT NULL,
  `is_tab` tinyint(1) NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `parent_category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tools_category_parent_category_id_e6e86c2a_fk_tools_category_id` (`parent_category_id`),
  CONSTRAINT `tools_category_parent_category_id_e6e86c2a_fk_tools_category_id` FOREIGN KEY (`parent_category_id`) REFERENCES `tools_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4
```

```
CREATE TABLE `tools_url` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `desc` longtext,
  `url` varchar(200) NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tools_url_category_id_76ded962_fk_tools_category_id` (`category_id`),
  CONSTRAINT `tools_url_category_id_76ded962_fk_tools_category_id` FOREIGN KEY (`category_id`) REFERENCES `tools_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=195 DEFAULT CHARSET=utf8mb4
```

```
USE `tools`;
CREATE VIEW `tools_view` 
AS (select `c`.`id`,`c`.`name`,`c`.`desc`,`c`.`url`,`a`.`id` AS `category_id`,`a`.`name` AS `category_name`,
`a`.`parent_category_id`,`b`.`name` AS `parent_category_name` 
from `tools_url` `c` 
left join `tools_category` `a` on (`a`.`id` = `c`.`category_id`)
left join `tools_category` `b` on (`b`.`id` = `a`.`parent_category_id`))
```