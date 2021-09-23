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

-- category table
create table category_attributes(
	idx INT NOT NULL AUTO_INCREMENT,
    category_en VARCHAR(50) not null,
    category_ko VARCHAR(50) not null,
    code INT NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- color table
create table color_attributes(
	idx INT NOT NULL AUTO_INCREMENT,
    attribute_en varchar(50) not null,
    attribute_ko varchar(50) not null,
    code varchar(50) null default '0',
    primary key(idx)
);

-- detail table
create table detail_attributes(
    idx INT NOT NULL AUTO_INCREMENT,
    attribute_en VARCHAR(50) NOT NULL,
    attribute_ko VARCHAR(50) NOT NULL,
    code varchar(50) null default '0',
    primary key(idx)
);

--print table
create table print_attributes(
    idx INT NOT NULL AUTO_INCREMENT,
    attribute_en VARCHAR(50) NOT NULL,
    attribute_ko VARCHAR(50) NOT NULL,
    code varchar(50) null default '0',
    primary key(idx)
);

-- material table
create table material_attributes(
    idx INT NOT NULL AUTO_INCREMENT,
    attribute_en VARCHAR(50) NOT NULL,
    attribute_ko VARCHAR(50) NOT NULL,
    code VARCHAR(50) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- sleevelength table
create table sleevelength_attributes(
    idx INT NOT NULL AUTO_INCREMENT,
    attribute_en VARCHAR(50) NOT NULL,
    attribute_ko VARCHAR(50) NOT NULL,
    code VARCHAR(50) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- neckline table
create table neckline_attributes(
    idx INT NOT NULL AUTO_INCREMENT,
    attribute_en VARCHAR(50) NOT NULL,
    attribute_ko VARCHAR(50) NOT NULL,
    code VARCHAR(50) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- collar table
create table collar_attributes(
    idx INT NOT NULL AUTO_INCREMENT,
    attribute_en VARCHAR(50) NOT NULL,
    attribute_ko VARCHAR(50) NOT NULL,
    code VARCHAR(50) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- fit table
create table fit_attributes(
    idx INT NOT NULL AUTO_INCREMENT,
    attribute_en VARCHAR(50) NOT NULL,
    attribute_ko VARCHAR(50) NOT NULL,
    code VARCHAR(50) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- shape table
create table shape_attributes(
    idx INT NOT NULL AUTO_INCREMENT,
    attribute_en VARCHAR(50) NOT NULL,
    attribute_ko VARCHAR(50) NOT NULL,
    code VARCHAR(50) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- silhouette table
create table silhouette_attributes(
    idx INT NOT NULL AUTO_INCREMENT,
    attribute_en VARCHAR(50) NOT NULL,
    attribute_ko VARCHAR(50) NOT NULL,
    code VARCHAR(50) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

create table search_log(
	idx INT NOT NULL AUTO_INCREMENT,
    s_type VARCHAR(5) not null, -- 검색타입 (트렌드 = tn, 의류 = co, 크롤링 = cl, 통계 = st)
    user_id VARCHAR(50) not null,	-- 검색한 user id
    result VARCHAR(10000),
    c_date datetime NOT NULL DEFAULT current_timestamp,
    PRIMARY KEY(idx)
);