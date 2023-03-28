create table student
(
    sid     integer auto_increment primary key,
    name    text not null,
    email   text,
    program text not null
);

create table instructor
(
    iid        integer auto_increment primary key,
    name       text not null,
    email      text,
    department text not null
);

create table course
(
    cid     integer auto_increment primary key,
    name    text not null,
    code    text,
    credits integer
);

create table offering
(
    oid      integer auto_increment primary key,
    semester char                            not null,
    year     integer                         not null,
    section  varchar(2)                      not null,
    cid      integer references course (cid) not null,
    iid      integer references instructor (iid),
    unique (semester, year, section, cid)
);

create table enrollment
(
    sid integer references student (sid)  not null,
    oid integer references offering (oid) not null,
    primary key (sid, oid)
);

insert into student(sid, name, email, program)
values ('1', 'John', 'john@example.com', 'CS'),
       ('2','Jane', 'jane@example.com', 'SE'),
       ('3','Joe', 'joe@example.com', 'CS'),
       ('4','Janet', 'janet@example.com', 'CS');



insert into instructor(iid,name, email, department)
values ('1','Denis', 'denis@example.com', 'CS'),
       ('2','Alice', 'alice@example.com', 'CS'),
       ('3','Bob', 'bob@example.com', 'CS');

insert into course(cid,name, code, credits)
values ('1','Databases', 'DB', 4),
       ('2','Web Programming', 'WP', 3),
       ('3','Security', 'SEC', 3);

insert into offering(oid,semester, year, section, cid, iid)
values ('1','W', 2020, 'A', 1, 1),
       ('2','W', 2020, 'B', 1, 2),
       ('3','W', 2019, 'A', 1, 2),
       ('4','W', 2020, 'C', 2, 1),
       ('5','W', 2020, 'D', 2, 1),
       ('6','F', 2019, 'B', 2, 1),
       ('7','S', 2020, 'A', 2, null);


insert into enrollment
values (1, 1),
       (1, 4),
       (2, 2),
       (2, 4),
       (3, 4),
       (3, 6);
