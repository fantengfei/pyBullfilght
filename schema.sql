drop table if exists login;
create table login (
  id integer primary key autoincrement,
  openid  char(100) not null,
  session char(100) not null
);