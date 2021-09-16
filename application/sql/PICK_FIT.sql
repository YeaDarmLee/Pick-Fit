CREATE DATABASE PICK_FIT;

-- user 기본정보
create table user_info(
	idx INT NOT NULL AUTO_INCREMENT,
    id VARCHAR(50) not null,
    pw VARCHAR(100) not null,
    userNm VARCHAR(200) not null,
    age int not null,
    gender int not null,
    height int not null,
    weight int not null,
    face_shape int null DEFAULT 0,
    body_shape int null DEFAULT 0,
    style int null DEFAULT 0,
    skin_tone int null DEFAULT 0,
    hair int null DEFAULT 0,
    c_date datetime NOT NULL DEFAULT current_timestamp,
    PRIMARY KEY(idx)
);

-- contact 메시지 전송시 저장되는 table
create table contact_info(
	idx INT NOT NULL AUTO_INCREMENT,
    userNm VARCHAR(200) not null,
    content VARCHAR(2000) not null,
    c_date datetime NOT NULL DEFAULT current_timestamp,
    PRIMARY KEY(idx)
);

-- recommend 검색로그 기록 table (미완성)
create table search_log(
	idx INT NOT NULL AUTO_INCREMENT,
    s_type VARCHAR(5) not null, -- 검색타입 (트렌드 = tn, 의류 = co, 크롤링 = cl, 통계 = st)
    user_id VARCHAR(50) not null,
    c_date datetime NOT NULL DEFAULT current_timestamp,
    PRIMARY KEY(idx)
);