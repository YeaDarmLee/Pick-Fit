CREATE DATABASE PICK_FIT;

-- 크롤링 form 저장 테이블
create table crawling_form(
	id INT NOT NULL AUTO_INCREMENT,
	title VARCHAR(500),
	url VARCHAR(1000),
    meta_tag VARCHAR(2000),
    meta_class VARCHAR(2000),
    c_date datetime NOT NULL DEFAULT current_timestamp,
    PRIMARY KEY(id)
);