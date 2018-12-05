-- auto-generated definition

DROP TABLE IF EXISTS t_role;

CREATE TABLE t_role
(
  id            BIGINT(16) NOT NULL AUTO_INCREMENT,
  name          VARCHAR(32) NOT NULL,
  description   VARCHAR(64) DEFAULT NULL,
  permissions   INT(5)      DEFAULT NULL,
  is_default    Boolean     DEFAULT FALSE,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO t_role VALUES (1,'User','Follow, Comment, Post',1, TRUE, sysdate());
INSERT INTO t_role VALUES (2,'Administrator','Follow, Comment, Post, User, Forbidden',2, FALSE, sysdate());


DROP TABLE IF EXISTS t_user;

CREATE TABLE t_user
(
  id            BIGINT(16)  NOT NULL AUTO_INCREMENT,
  username      VARCHAR(32) NOT NULL,
  role_id       BIGINT(16)  DEFAULT NULL,
  password_hash VARCHAR(256) NOT NULL,
  name          VARCHAR(18) DEFAULT NULL,
  tel           VARCHAR(18) DEFAULT NULL,
  email         VARCHAR(32) DEFAULT NULL,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE (username),
  CONSTRAINT user_role_id FOREIGN KEY (role_id) REFERENCES t_role (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO t_user VALUES (1,'test',1,'pbkdf2:sha256:50000$5In9uW8H$2f1aebe35025d88aa8f325c19d836f013627d3e716bd320c6dff4fd26472c3aa', 'TestUser',NULL,NULL, sysdate());


DROP TABLE IF EXISTS t_article;
CREATE TABLE t_article (
  id         BIGINT(16)   NOT NULL AUTO_INCREMENT,
  title      VARCHAR(128) DEFAULT NULL,
  body       TEXT         DEFAULT NULL,
  body_html  TEXT         DEFAULT NULL,
  author_id  BIGINT(16)   DEFAULT NULL,
  is_forbidden Boolean    DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT article_author_id FOREIGN KEY (author_id) REFERENCES t_user (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO t_article VALUES (1,'My First Article', 'This is my first article',NULL,1, sysdate());


DROP TABLE IF EXISTS t_comment;
CREATE TABLE t_comment (
  id         BIGINT(16) NOT NULL AUTO_INCREMENT,
  body       TEXT       DEFAULT NULL,
  body_html  TEXT       DEFAULT NULL,
  author_id  BIGINT(16) DEFAULT NULL,
  article_id BIGINT(16) DEFAULT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT comment_author_id FOREIGN KEY (author_id) REFERENCES t_user (id),
  CONSTRAINT comment_article_id FOREIGN KEY (article_id) REFERENCES t_article (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS t_follow;
CREATE TABLE t_follow
(
  id            BIGINT(16)  NOT NULL AUTO_INCREMENT,
  follower_id   BIGINT(16)  NOT NULL,
  following_id  BIGINT(16)  NOT NULL,
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT follow_follower_id FOREIGN KEY (follower_id) REFERENCES t_user (id),
  CONSTRAINT follow_following_id FOREIGN KEY (following_id) REFERENCES t_user (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

