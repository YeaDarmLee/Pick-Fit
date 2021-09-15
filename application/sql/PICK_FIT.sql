CREATE DATABASE PICK_FIT;

-- user 기본정보
create table user_info(
	idx INT NOT NULL AUTO_INCREMENT,
    id VARCHAR(500) not null,
    pw VARCHAR(500) not null,
    userNm VARCHAR(200) not null,
    age int not null,
    gender int not null,
    height VARCHAR(50) not null,
    weight VARCHAR(50) not null,
    face_shape int null DEFAULT 0,
    body_shape int null DEFAULT 0,
    style int null DEFAULT 0,
    skin_tone int null DEFAULT 0,
    hair int null DEFAULT 0,
    PRIMARY KEY(idx)
);

-- contact table
create table contact_info(
	idx INT NOT NULL AUTO_INCREMENT,
    userNm VARCHAR(200) not null,
    content VARCHAR(2000) not null,
    c_date datetime NOT NULL DEFAULT current_timestamp,
    PRIMARY KEY(idx)
);