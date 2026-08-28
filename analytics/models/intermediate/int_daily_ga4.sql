select
    activity_date,
    sum(sessions) as sessions,
    sum(users) as active_user_days,
    sum(product_views) as product_views,
    sum(add_to_carts) as add_to_carts,
    sum(begin_checkouts) as begin_checkouts,
    sum(purchases) as tracked_purchases,
    sum(purchase_revenue_sar) as tracked_purchase_revenue_sar
from {{ ref('stg_ga4_daily') }}
group by 1
