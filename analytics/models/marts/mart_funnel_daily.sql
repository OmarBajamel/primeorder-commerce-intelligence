select
    activity_date,
    device,
    channel,
    concat(activity_date, '|', device, '|', channel) as funnel_key,
    sum(sessions) as sessions,
    sum(product_views) as product_views,
    sum(add_to_carts) as add_to_carts,
    sum(begin_checkouts) as begin_checkouts,
    sum(purchases) as tracked_purchases,
    sum(product_views)::double / nullif(sum(sessions), 0) as product_view_rate,
    sum(add_to_carts)::double / nullif(sum(product_views), 0) as add_to_cart_rate,
    sum(begin_checkouts)::double / nullif(sum(add_to_carts), 0) as checkout_start_rate,
    sum(purchases)::double / nullif(sum(sessions), 0) as purchase_conversion_rate
from {{ ref('stg_ga4_daily') }}
group by 1, 2, 3
