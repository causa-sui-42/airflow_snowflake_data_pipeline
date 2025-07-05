
with events as (
    select * from {{ ref('raw_events') }}
)
select
    user_id,
    event_type,
    count(*) as event_count,
    date_trunc('day', event_time) as event_day
from events
group by user_id, event_type, event_day
