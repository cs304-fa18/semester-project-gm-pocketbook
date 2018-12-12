use pbmod;

drop table if exists `character`;
drop table if exists `notes`;
drop table if exists `towns`;
drop table if exists `misc`;
drop table if exists `kind`;
drop table if exists `usercomp`;
drop table if exists `comp`;
drop table if exists `usertocamp`;
drop table if exists `campaign`;
drop table if exists `user`;

create table user(
    uid int auto_increment,
    username varchar(30) unique,
    hashed char(60),
    primary key(uid)
) ENGINE=InnoDB;

create table campaign(
    cid int auto_increment,
    name varchar (30),
    primary key(cid)
) ENGINE=InnoDB;

create table usertocamp(
    dm enum('yes', 'no'),
    cid int,
    uid int,
    primary key(cid, uid),
    foreign key (cid) references campaign (cid) on delete cascade on update cascade,
    foreign key (uid) references user (uid) on delete cascade on update cascade
) ENGINE=InnoDB;

create table comp(
    cid int,
    comptype enum('character', 'notes', 'towns', 'misc') not null,
    primary key (cid,comptype)
) ENGINE=InnoDB;

create table `character`(
    cid int auto_increment,
    name varchar(30), 
    class varchar(30), 
    race varchar(30), 
    alignment varchar(30), 
    file varchar(30), 
    campid int not null,
    uid int not null,
    primary key (cid),
    foreign key (cid) references comp(cid) on delete cascade on update cascade,
    foreign key (campid) references campaign (cid) on delete cascade on update cascade,
    foreign key (uid) references user (uid) on delete cascade on update cascade
) ENGINE=InnoDB;
    
create table notes(
    nid int auto_increment,
    name varchar(30), 
    body text, 
    file varchar(30), 
    campid int not null,
    uid int not null,
    primary key (nid),
    foreign key (nid) references comp(cid) on delete cascade on update cascade,
    foreign key (campid) references campaign (cid) on delete cascade on update cascade,
    foreign key (uid) references user (uid) on delete cascade on update cascade
) ENGINE=InnoDB;

create table towns(
    tid int auto_increment,
    name varchar(30), 
    descrip text, 
    map varchar(30), 
    file varchar(30), 
    campid int not null,
    uid int not null,
    primary key (tid),
    foreign key (tid) references comp(cid) on delete cascade on update cascade,
    foreign key (campid) references campaign (cid) on delete cascade on update cascade,
    foreign key (uid) references user (uid) on delete cascade on update cascade
) ENGINE=InnoDB;

create table kind(
    kid int auto_increment,
    name varchar(30) unique, 
    primary key (kid)
) ENGINE=InnoDB;

create table misc(
    mscid int auto_increment,
    name varchar(30), 
    descrip text, 
    file varchar(30), 
    campid int not null,
    uid int not null,
    kid int,
    primary key (mscid),
    foreign key (mscid) references comp(cid) on delete cascade on update cascade,
    foreign key (campid) references campaign (cid) on delete cascade on update cascade,
    foreign key (kid) references kind (kid) on delete cascade on update cascade,
    foreign key (uid) references user (uid) on delete cascade on update cascade
) ENGINE=InnoDB;

create table usercomp(
    cid int not null,
    uid int not null, 
    comptype enum('character', 'notes', 'towns', 'misc') not null,
    primary key (cid, uid, comptype),
    foreign key (cid, comptype) references comp (cid, comptype) on delete cascade on update cascade,
    foreign key (uid) references user (uid) on delete cascade on update cascade
) ENGINE=InnoDB;
