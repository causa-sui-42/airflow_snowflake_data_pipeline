
with source as (
    select * from {{ ref('raw_users') }}
)
select
    id,
    upper(name) as name,
    lower(email) as email
from source
where name is not null and email is not null
