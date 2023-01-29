CREATE DATABASE pictures;

CREATE USER 'mbit'@'%' IDENTIFIED BY 'mbit';
GRANT ALL PRIVILEGES ON pictures.* TO 'mbit'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;

USE pictures;

CREATE TABLE pictures (
  id int(11) NOT NULL,
  path varchar(200) NOT NULL,
  date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 
COMMENT='Picture table for save images from API';

CREATE TABLE tags (
  tag varchar(32) NOT NULL,
  picture_id int(11) NOT NULL,
  confidence float NOT NULL,
  date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 
COMMENT='Tag table for save tags asociated to pictures';

ALTER TABLE pictures
  ADD PRIMARY KEY (id);

ALTER TABLE tags
  ADD PRIMARY KEY (tag,picture_id);

ALTER TABLE pictures
  MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

ALTER TABLE tags
ADD FOREIGN KEY (picture_id) REFERENCES pictures(id);

