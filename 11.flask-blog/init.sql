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

INSERT INTO t_role VALUES (1,'普通用户','发布文章，管理文章',1, TRUE, sysdate());


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

INSERT INTO t_user VALUES (1,'test',1,'$6$rounds=656000$k1mATcIxrC9GiQtg$9H82DiOC..z8AxDiqU0hUI9idppt/rPEtxgdScPmAyvjV2HJwGIzEq/HLdp6tYx6sg.PMKie/ldx4U9yN.ZPj0', 'TestUser',NULL,NULL, sysdate());


DROP TABLE IF EXISTS t_article;
CREATE TABLE t_article (
  id         BIGINT(16)   NOT NULL AUTO_INCREMENT,
  title      VARCHAR(128) DEFAULT NULL,
  body       TEXT         DEFAULT NULL,
  body_html  TEXT         DEFAULT NULL,
  author_id  BIGINT(16)   DEFAULT NULL,
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
