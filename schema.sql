drop table if exists nyheter;

create table nyheter (
	id integer primary key autoincrement,
	tittel text not null,
	nyhet text not null,
	forfatter text not null,
	dagens int not null
);
