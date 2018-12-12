insert into user(username,hashed,uid) values ('daniela','$2b$12$z54wAfIGMMTwpcd7uu0JAO8rDdElvfsi4../hOBx5tD5LmKKX25US',1);
insert into user(username,hashed,uid) values ('heather','$2b$12$z54wAfIGMMTwpcd7uu0JAO8rDdElvfsi4../hOBx5tD5LmKKX25US',2);
insert into user(username,hashed,uid) values ('helen','$2b$12$z54wAfIGMMTwpcd7uu0JAO8rDdElvfsi4../hOBx5tD5LmKKX25US',3);
insert into user(username,hashed,uid) values ('margaret-anne','$2b$12$z54wAfIGMMTwpcd7uu0JAO8rDdElvfsi4../hOBx5tD5LmKKX25US',4);
insert into user(username,hashed,uid) values ('alex','$2b$12$z54wAfIGMMTwpcd7uu0JAO8rDdElvfsi4../hOBx5tD5LmKKX25US',5);
insert into user(username,hashed,uid) values ('axel','$2b$12$z54wAfIGMMTwpcd7uu0JAO8rDdElvfsi4../hOBx5tD5LmKKX25US',6);
insert into user(username,hashed,uid) values ('bel','$2b$12$z54wAfIGMMTwpcd7uu0JAO8rDdElvfsi4../hOBx5tD5LmKKX25US',7);
insert into user(username,hashed,uid) values ('six','$2b$12$z54wAfIGMMTwpcd7uu0JAO8rDdElvfsi4../hOBx5tD5LmKKX25US',8);

insert into campaign(name,cid) values ('Team Dumbass',1);

insert into usertocamp(dm,cid,uid) values ('yes',1,1);
insert into usertocamp(dm,cid,uid) values ('no',1,2);
insert into usertocamp(dm,cid,uid) values ('no',1,3);
insert into usertocamp(dm,cid,uid) values ('no',1,4);
insert into usertocamp(dm,cid,uid) values ('no',1,5);
insert into usertocamp(dm,cid,uid) values ('no',1,6);
insert into usertocamp(dm,cid,uid) values ('no',1,7);
insert into usertocamp(dm,cid,uid) values ('no',1,8);

insert into comp(cid, comptype) values(1,'character');
insert into comp(cid, comptype) values(2,'character');
insert into comp(cid, comptype) values(3,'character');
insert into comp(cid, comptype) values(4,'character');
insert into comp(cid, comptype) values(5,'character');
insert into comp(cid, comptype) values(6,'character');
insert into comp(cid, comptype) values(7,'character');
insert into comp(cid, comptype) values(8,'character');
insert into comp(cid, comptype) values(9,'character');
insert into comp(cid, comptype) values(10,'character');

insert into comp(cid, comptype) values(1,'notes');
insert into comp(cid, comptype) values(2,'notes');
insert into comp(cid, comptype) values(3,'notes');

insert into comp(cid, comptype) values(1,'towns');
insert into comp(cid, comptype) values(2,'towns');
insert into comp(cid, comptype) values(3,'towns');
insert into comp(cid, comptype) values(4,'towns');
insert into comp(cid, comptype) values(5,'towns');
insert into comp(cid, comptype) values(6,'towns');
insert into comp(cid, comptype) values(7,'towns');
insert into comp(cid, comptype) values(8,'towns');

insert into comp(cid, comptype) values(1,'misc');

insert into `character`(cid,name,class,race,alignment,campid,uid)
    values (1,'Vriska Serket','Wizard','High elf','Chaotic Neutral',1,1);
insert into `character`(cid,name,class,race,alignment,campid,uid)
    values (2,'Shae','N/A','Human','Lawful Good',1,1);
insert into `character`(cid,name,class,race,alignment,campid,uid)
    values (3,'Sahm Harwitz','Druid','Half-elf','Neutral Good',1,1);

insert into `character`(cid,name,class,race,alignment,campid,uid)
    values (4,'Shava Nailo','Wizard','Sun elf','Chaotic Good',1,2);
insert into `character`(cid,name,class,race,alignment,campid,uid)
    values (5,'Hermes','Wizard','Aarakocra','True Neutral',1,3);
insert into `character`(cid,name,class,race,alignment,campid,uid)
    values (6,'Tally','Wizard','Drow','Lawful Good',1,4);
insert into `character`(cid,name,class,race,alignment,campid,uid)
    values (7,'Tseven','Cleric','High elf','True Neutral',1,5);
insert into `character`(cid,name,class,race,alignment,campid,uid)
    values (8,'Quill','Fighter','Human','Lawful Good',1,6);
insert into `character`(cid,name,class,race,alignment,campid,uid)
    values (9,'Jokaryn Vypuur','Fighter','Dragonborn','Chaotic Good',1,7);
insert into `character`(cid,name,class,race,alignment,campid,uid)
    values (10,'Ailith Piper','Bard','Half-elf','Chaotic Neutral',1,8);
   
insert into notes(nid,name,body,campid,uid)
    values (1,"Letter Clue 1",
        "Good work with securing the key. Go to the treehouse, await comms. Take 10 coins.",
        1,1);
insert into notes(nid,name,body,campid,uid)
    values (2,"Letter Clue 2",
        "Take 13 coins. Your next location is on the map. Don't come back, just go where I marked out for you. Take a few days more in the treehouse if you need.",
        1,1);
insert into notes(nid,name,body,campid,uid)
    values(3,"Quill to Tally Apology Letter",
    "Hi Tally. Really sorry about all that murder. I know you won't talk to me and I don't want to spook you, but please know I am truly sorry for scaring you.",
    1,6);

insert into towns(tid,name,descrip,map,campid,uid)
    values(1,'Arbora','Living, hollow tree with a mysterious power coming from the souls of those who died in this area. Basically a operates as a resting place for travelers. Does not like murder.',
    'arbora.png',1,1);
insert into towns(tid,name,descrip,map,campid,uid)
    values(2,'Trajos','Deserted giant Trader Joes where Tseven is from.',
    'trajos.png',1,5);
insert into towns(tid,name,descrip,map,campid,uid)
    values(3,'Traia','Pacifist lesbian farming commune built in the ruins of an ancient megalopolis that Jokaryn hails form.',
    'traia.png',1,7);
insert into towns(tid,name,descrip,map,campid,uid)
    values(4, 'Ellia','Gated community for snobby elves that is also a settler colonial state hidden behind a waterfall. Shava is from here.',
    'ellia.png',1,2);
insert into towns(tid,name,descrip,map,campid,uid)
    values(5,'Chorrea','Discrete home of small funky skeleton biker gang that adopts abandoned babies and trains them in music. Piper comes from here.',
    'chorrea.png',1,8);
insert into towns(tid,name,descrip,map,campid,uid)
    values(6,'Castle Ash','Mad Max-style neo-feudalism ruled by humans who claim to be descended from pre-apocalypse demigods operated out of a surprisingly well-preserved castle.',
    'castle-ash.png',1,6);
insert into towns(tid,name,descrip,map,campid,uid)
    values(7,'Kya','Underground colony of drows who live in interconnected caves.',
    'kya.png',1,4);
insert into towns(tid,name,descrip,map,campid,uid)
    values(8,'Ncepton','Deserted megalopolis at the edges of a magical wasteland. Ghosts abound.',
    'ncepton.png',1,1);
    
insert into kind(kid,name) values(1,"file");

insert into misc(mscid,name,descrip,file,campid,uid,kid)
    values(1,"Piper's Bagpipe Song","MeGaLoVaNia but on bagpipes",'bagpipe-megalovania.mp3',1,8,1);

insert into usercomp(cid,uid,comptype) values(1,2,'character');
insert into usercomp(cid,uid,comptype) values(1,4,'character');

insert into usercomp(cid,uid,comptype) values(2,5,'character');
insert into usercomp(cid,uid,comptype) values(2,3,'character');

insert into usercomp(cid,uid,comptype) values(3,6,'character');
insert into usercomp(cid,uid,comptype) values(3,5,'character');

insert into usercomp(cid,uid,comptype) values(4,7,'character');
insert into usercomp(cid,uid,comptype) values(4,2,'character');

insert into usercomp(cid,uid,comptype) values(5,8,'character');
insert into usercomp(cid,uid,comptype) values(5,4,'character');

insert into usercomp(cid,uid,comptype) values(6,3,'character');
insert into usercomp(cid,uid,comptype) values(6,7,'character');

insert into usercomp(cid,uid,comptype) values(7,2,'character');
insert into usercomp(cid,uid,comptype) values(7,3,'character');

insert into usercomp(cid,uid,comptype) values(8,6,'character');
insert into usercomp(cid,uid,comptype) values(8,5,'character');

insert into usercomp(cid,uid,comptype) values(9,7,'character');
insert into usercomp(cid,uid,comptype) values(9,2,'character');

insert into usercomp(cid,uid,comptype) values(10,6,'character');
insert into usercomp(cid,uid,comptype) values(10,3,'character');

insert into usercomp(cid,uid,comptype) values(1,7,'notes');
insert into usercomp(cid,uid,comptype) values(1,8,'notes');

insert into usercomp(cid,uid,comptype) values(2,2,'notes');
insert into usercomp(cid,uid,comptype) values(2,4,'notes');

insert into usercomp(cid,uid,comptype) values(3,3,'notes');
insert into usercomp(cid,uid,comptype) values(3,6,'notes');

insert into usercomp(cid,uid,comptype) values(1,2,'towns');
insert into usercomp(cid,uid,comptype) values(1,7,'towns');

insert into usercomp(cid,uid,comptype) values(2,8,'towns');
insert into usercomp(cid,uid,comptype) values(2,6,'towns');

insert into usercomp(cid,uid,comptype) values(3,5,'towns');
insert into usercomp(cid,uid,comptype) values(3,4,'towns');

insert into usercomp(cid,uid,comptype) values(4,7,'towns');
insert into usercomp(cid,uid,comptype) values(4,3,'towns');

insert into usercomp(cid,uid,comptype) values(5,4,'towns');
insert into usercomp(cid,uid,comptype) values(5,6,'towns');

insert into usercomp(cid,uid,comptype) values(6,4,'towns');
insert into usercomp(cid,uid,comptype) values(6,8,'towns');

insert into usercomp(cid,uid,comptype) values(7,3,'towns');
insert into usercomp(cid,uid,comptype) values(7,2,'towns');

insert into usercomp(cid,uid,comptype) values(8,6,'towns');
insert into usercomp(cid,uid,comptype) values(8,4,'towns');

insert into usercomp(cid,uid,comptype) values(1,2,'misc');
insert into usercomp(cid,uid,comptype) values(1,3,'misc');