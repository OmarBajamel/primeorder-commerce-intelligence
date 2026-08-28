with expected(event_name) as (
    values ('view_item_list'), ('select_item'), ('view_item'), ('add_to_cart'), ('remove_from_cart'),
           ('view_cart'), ('begin_checkout'), ('add_shipping_info'), ('add_payment_info'), ('purchase'), ('refund')
), actual as (
    select distinct event_name from {{ ref('stg_events') }}
)
select expected.event_name
from expected left join actual using (event_name)
where actual.event_name is null
