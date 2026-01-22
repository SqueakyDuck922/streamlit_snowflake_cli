use role dev_streamlit_demo_secadmin;

use role accountadmin;

use warehouse DEV_DEVELOPER_WH;

use schema DEV_STREAMLIT_DEMO.SCHEMA1;

create or replace hybrid table taxo_categories(
    id int primary key,
    name string,
    parent_id int
)

;


insert into taxo_categories(id, name, parent_id)
values
(1, 'parent 1',0)
,(2, 'parent 2',0)
,(3, 'parent 3',0)
,(4,'sub 1_1',1)
,(5,'sub 1_2',1)
,(6,'sub 1_2',1)
,(7,'sub 3_1',3)

;

select * from  schema1.taxo_categories;
;

create or replace hybrid table taxo_records (
record_id int identity(1,1) primary key,
taxo_id int,
value1 int,
value2 text,
foreign key (taxo_id) references taxo_categories(id)

)
;


insert into taxo_records(taxo_id,value1,value2)
values
(1,33,'chicken')

;

select * from taxo_records