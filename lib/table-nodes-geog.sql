-- Table: public.nodes_geog

CREATE TABLE IF NOT EXISTS public.nodes_geog
(
    node_id integer,
    coord point,
    geom geometry(Point,4326),
    geog geography(Point,4326)
);

