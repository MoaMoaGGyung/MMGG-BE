SET GLOBAL time_zone='+09:00';
SET time_zone='+09:00';

use mysql;
create user 'root'@'%' identified by 'dlatl';
grant all privileges on *.* to 'root'@'%';
flush privileges;

DROP SCHEMA IF EXISTS mmgg;
CREATE SCHEMA mmgg;