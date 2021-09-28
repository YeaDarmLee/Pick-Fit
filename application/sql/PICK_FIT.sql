-- 가비아 DB명
CREATE DATABASE dbpublic0917;

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
    dev int not null DEFAULT 0,
    PRIMARY KEY(idx)
);

-- 관리자일 경우 아래 쿼리 실행
UPDATE user_info SET dev = 1 WHERE id = '';

-- contact table
create table contact_info(
	idx INT NOT NULL AUTO_INCREMENT,
    userNm VARCHAR(200) not null,
    content VARCHAR(2000) not null,
    c_date datetime NOT NULL DEFAULT current_timestamp,
    PRIMARY KEY(idx)
);

-- category table
create table at_category(
	idx INT NOT NULL AUTO_INCREMENT,
    en VARCHAR(50) not null,
    ko VARCHAR(50) not null,
    code VARCHAR(10) not null default '0',
    PRIMARY KEY(idx)
);

-- color table
create table at_color(
	idx INT NOT NULL AUTO_INCREMENT,
    en varchar(50) not null,
    ko varchar(50) not null,
    code varchar(10) null default '0',
    primary key(idx)
);

-- detail table
create table at_detail(
    idx INT NOT NULL AUTO_INCREMENT,
    en VARCHAR(50) NOT NULL,
    ko VARCHAR(50) NOT NULL,
    code varchar(10) null default '0',
    primary key(idx)
);

--print table
create table at_print(
    idx INT NOT NULL AUTO_INCREMENT,
    en VARCHAR(50) NOT NULL,
    ko VARCHAR(50) NOT NULL,
    code varchar(10) null default '0',
    primary key(idx)
);

-- material table
create table at_material(
    idx INT NOT NULL AUTO_INCREMENT,
    en VARCHAR(50) NOT NULL,
    ko VARCHAR(50) NOT NULL,
    code VARCHAR(10) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- sleevelength table
create table at_sleevelength(
    idx INT NOT NULL AUTO_INCREMENT,
    en VARCHAR(50) NOT NULL,
    ko VARCHAR(50) NOT NULL,
    code VARCHAR(10) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- neckline table
create table at_neckline(
    idx INT NOT NULL AUTO_INCREMENT,
    en VARCHAR(50) NOT NULL,
    ko VARCHAR(50) NOT NULL,
    code VARCHAR(10) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- collar table
create table at_collar(
    idx INT NOT NULL AUTO_INCREMENT,
    en VARCHAR(50) NOT NULL,
    ko VARCHAR(50) NOT NULL,
    code VARCHAR(10) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- fit table
create table at_fit(
    idx INT NOT NULL AUTO_INCREMENT,
    en VARCHAR(50) NOT NULL,
    ko VARCHAR(50) NOT NULL,
    code VARCHAR(10) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- shape table
create table at_shape(
    idx INT NOT NULL AUTO_INCREMENT,
    en VARCHAR(50) NOT NULL,
    ko VARCHAR(50) NOT NULL,
    code VARCHAR(10) NULL DEFAULT '0',
    PRIMARY KEY(idx)
);

-- silhouette table
create table at_silhouette(
    idx INT NOT NULL AUTO_INCREMENT,
    en VARCHAR(50) NOT NULL,
    ko VARCHAR(50) NOT NULL,
    code VARCHAR(10) NULL DEFAULT '0',
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

-- 의류 정보 데이터
create table clothing_data (
	idx INT NOT NULL AUTO_INCREMENT,
    file_name VARCHAR(50) NOT NULL DEFAULT 0,
    img LONGBLOB,
    title VARCHAR(50) NOT NULL DEFAULT 0,
    style VARCHAR(50) NOT NULL DEFAULT 0,
    style_sub VARCHAR(50) NOT NULL DEFAULT 0,
    length VARCHAR(50) NOT NULL DEFAULT 0,
    color VARCHAR(50) NOT NULL DEFAULT 0,
    color_sub VARCHAR(50) NOT NULL DEFAULT 0,
    category VARCHAR(50) NOT NULL DEFAULT 0,
    collar VARCHAR(50) NOT NULL DEFAULT 0,
    sleeve VARCHAR(50) NOT NULL DEFAULT 0,
    detail VARCHAR(50) NOT NULL DEFAULT 0,
    material VARCHAR(50) NOT NULL DEFAULT 0,
    pattern VARCHAR(50) NOT NULL DEFAULT 0,
    neckline VARCHAR(50) NOT NULL DEFAULT 0,
    fit VARCHAR(50) NOT NULL DEFAULT 0,
    safe VARCHAR(50) NOT NULL DEFAULT 0,
    silhouette VARCHAR(50) NOT NULL DEFAULT 0,
    PRIMARY KEY(idx)
);