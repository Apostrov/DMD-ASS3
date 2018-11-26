create table if not exists location (
  GPS varchar (100) not null,
  city varchar (50),
  street varchar (50),
  zip_code integer,

  primary key (GPS)
);

create table if not exists charging_station (
  UID integer primary key autoincrement,
  available_sockets integer,
  price integer,
  time_of_charging integer,
  GPS varchar (100) not null,

  foreign key (GPS) references location (GPS)
);

create table if not exists plug (
  UID integer not null,
  shape varchar (50),
  size integer,

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
  WID integer primary key autoincrement,
  open_time time,
  close_time time,
  GPS varchar (100) not null,

  foreign key (GPS) references location (GPS)
);

create table if not exists car_part (
  part_ID integer primary key autoincrement,
  part_type varchar (40),
  car_type varchar (50),
  specifications varchar (150),

  foreign key (car_type) references car_type(car_type)
);

create table if not exists workshop_car_part (
  amount integer,
  part_ID integer not null,
  WID integer not null,

  foreign key (part_ID) references car_part (part_ID),
  foreign key (WID) references workshop (WID)
);

create table if not exists provider (
  PID integer primary key autoincrement,
  phone_number varchar (20),
  GPS varchar (100) not null,

  foreign key (gps) references location (GPS)
);

create table if not exists provide_car_parts (
  amount integer,
  part_ID integer not null,
  PID integer not null,
  WID integer not null,
  provided_date date,

  foreign key (part_ID) references car_part (part_ID),
  foreign key (PID) references provider (PID),
  foreign key (WID) references workshop (WID)
);

create table if not exists car_type (
  car_type varchar (50),

  primary key (car_type)
);

create table if not exists car (
  plate varchar(15) not null,
  car_type varchar(50) not null,
  broken boolean,
  charge_amount integer,
  GPS varchar (100),
  color varchar(40),

  primary key (plate),
  foreign key (car_type) references car_type(car_type)
);

create table if not exists ride (
  plate varchar(15) not null,
  username varchar (50) not null,
  coordinate_a varchar (100),
  coordinate_b varchar (100),
  using_start datetime,
  using_end datetime,

  foreign key (plate) references car (plate),
  foreign key (username) references customer (username)
);

create table if not exists charge (
  plate varchar(15) not null,
  UID integer not null,
  cost integer,
  charged_datetime datetime,

  foreign key (plate) references car (plate),
  foreign key (UID) references charging_station (UID)
);

create table if not exists repair (
  plate varchar(15) not null,
  WID integer not null,
  cost integer,
  repair_date date,

  foreign key (plate) references car (plate),
  foreign key (WID) references workshop (WID)
);