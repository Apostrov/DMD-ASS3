create table if not exists location (
  GPS varchar (100) not null,
  city varchar (50),
  street varchar (50),
  zip_code int,

  primary key (GPS)
);

create table if not exists charging_station (
  UID int not null,
  available_sockets int,
  price varchar (50),
  time_of_charging int,
  GPS varchar (100) not null,

  primary key (UID),
  foreign key (GPS) references location (GPS)
);

create table if not exists plug (
  UID int not null,
  shape varchar (50),
  size int,

  foreign key (UID) references charging_station (UID)
);

create table if not exists customer (
  username varchar (50) not null,
  fullname varchar (100),
  phone_number varchar (20),
  email varchar (60),
  GPS varchar (100) not null,

  primary key (username),
  foreign key (GPS) references location (GPS)
);

create table if not exists workshop (
  WID int not null,
  open_time time,
  close_time time,
  GPS varchar (100) not null,

  primary key (WID),
  foreign key (GPS) references location (GPS)
);

create table if not exists car_part (
  part_type varchar (40),
  car_type varchar (40),
  amount int,
  specifications varchar (150),
  WID int not null,

  foreign key (WID) references workshop (WID)
);

create table if not exists provider (
  phone_number varchar (20),
  PID int not null,
  GPS varchar (100) not null,

  primary key (PID),
  foreign key (gps) references location (GPS)
);

create table if not exists provide_car_parts (
  part_type varchar (40),
  car_type varchar (40),
  amount int,
  specifications varchar (150),
  PID int not null,
  WID int not null,
  provided_date date,

  foreign key (PID) references provider (PID),
  foreign key (WID) references workshop (WID)
);

create table if not exists car (
  plate varchar(15),
  type varchar (50),
  broken boolean,
  charge_amount int,
  GPS varchar (100),
  color varchar(40),

  primary key (plate)
);

create table if not exists ride (
  plate int not null,
  username varchar (50) not null,
  coordinate_a varchar (100),
  coordinate_b varchar (100),
  using_start datetime,
  using_end datetime,

  foreign key (plate) references car (plate),
  foreign key (username) references customer (username)
);

create table if not exists charge (
  plate int not null,
  UID int not null,
  charged_datetime datetime,

  foreign key (plate) references car (plate),
  foreign key (UID) references charging_station (UID)
);

create table if not exists repair (
  plate int not null,
  WID int not null,

  foreign key (plate) references car (plate),
  foreign key (WID) references workshop (WID)
);