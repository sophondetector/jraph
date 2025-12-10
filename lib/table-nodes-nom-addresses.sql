-- Table: public.nodes_nom_addresses

CREATE TABLE IF NOT EXISTS public.nodes_nom_addresses
(
    node_id integer,
    geocoded_address jsonb
);
