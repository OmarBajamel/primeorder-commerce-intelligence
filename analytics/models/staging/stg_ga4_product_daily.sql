select
    cast(date as date) as activity_date,
    cast(channel as varchar) as channel,
    cast(source as varchar) as source,
    cast(medium as varchar) as medium,
    cast(campaign as varchar) as campaign,
    lower(cast(device as varchar)) as device,
    cast(product_id as varchar) as product_id,
    cast(sessions as bigint) as sessions,
    cast(active_user_days as bigint) as active_user_days,
    cast(product_views as bigint) as product_views,
    cast(add_to_carts as bigint) as add_to_carts,
    cast(begin_checkouts as bigint) as begin_checkouts,
    cast(tracked_purchases as bigint) as tracked_purchases
from {{ ref('ga4_product_daily') }}
