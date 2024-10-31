create table templates
(
    tidx        serial
        constraint templates_pk
            primary key,
    templateid  uuid      default gen_random_uuid() not null,
    name        varchar   default ''::character varying,
    description varchar   default ''::character varying,
    content     varchar   default ''::character varying,
    created     timestamp default now(),
    modified    timestamp default now()
);

alter table templates
    owner to root;
