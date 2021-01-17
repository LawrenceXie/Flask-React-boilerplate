drop table if exists admin;
drop table if exists items;

create table admin (
  id integer primary key,
  key text not null,
  value text not null,
  format text not null
);

create table items (
  id text primary key not null,
  date_created integer not null,
  date_updated integer not null,
  'text' text not null
);

