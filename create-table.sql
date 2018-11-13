create table if not exists location (
  GPS varchar(100) not null,
  city varchar(50),
  street varchar(50),
  zip_code int,

  primary key (GPS)
);

create table if not exists charging_station (
  UID int not null,
  aviable_sockets int,
  price varchar(50),
  time_of_charging int,
  GPS varchar(100) not null,

  primary key (UID),
  foreign key (GPS) references location(GPS)
);

create table if not exists plug (
  UID int not null,
  shape varchar(50),
  size int,

  foreign key (UID) references charging_station(UID)
);
