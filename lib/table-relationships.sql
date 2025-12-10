-- Table: public.relationships

CREATE TABLE IF NOT EXISTS public.relationships
(
    _start integer NOT NULL,
    _end integer NOT NULL,
    _type character varying COLLATE pg_catalog."default",
    link character varying COLLATE pg_catalog."default",
    status character varying COLLATE pg_catalog."default",
    start_date character varying COLLATE pg_catalog."default",
    end_date character varying COLLATE pg_catalog."default",
    "sourceID" character varying COLLATE pg_catalog."default",
    edge_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 )
);

