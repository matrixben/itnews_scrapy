/* PostgreSQL */
create table news(
    news_id serial primary key,
    title text,
    tag text,
    publish_date timestamp with time zone,
    source_url text
);