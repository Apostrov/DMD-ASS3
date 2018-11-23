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
  timing_availability time,
  GPS varchar (100) not null,

  primary key (WID),
  foreign key (GPS) references location (GPS)
);

create table if not exists car_part (
  part_type varchar (40),
  car_type varchar (40),
  amount varchar (40),
  specifications varchar (150),
  id int not null,
  WID int not null,

  primary key (id),
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
  amount varchar (40),
  specifications varchar (150),
  PID int not null,
  WID int not null,

  foreign key (PID) references provider (PID),
  foreign key (WID) references workshop (WID)
);

create table if not exists car (
  CID int not null,
  type varchar (50),
  broken boolean,
  charge_amount int,
  GPS varchar (100),

  primary key (CID)
);

create table if not exists ride (
  CID int not null,
  username varchar (50) not null,
  coordinate_a varchar (100),
  coordinate_b varchar (100),

  foreign key (CID) references car (CID),
  foreign key (username) references customer (username)
);

create table if not exists charge (
  CID int not null,
  UID int not null,
  charged_datetime datetime,

  foreign key (CID) references car (CID),
  foreign key (UID) references charging_station (UID)
);

create table if not exists repair (
  CID int not null,
  WID int not null,

  foreign key (CID) references car (CID),
  foreign key (WID) references workshop (WID)
);