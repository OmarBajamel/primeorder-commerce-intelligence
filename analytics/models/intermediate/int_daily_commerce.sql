select
    activity_date,
    sum(sessions) as sessions,
    sum(users) as users,
    sum(product_views) as product_views,
    sum(add_to_carts) as add_to_carts,
    sum(begin_checkouts) as begin_checkouts,
    sum(purchases) as purchases,
    sum(units_sold) as units_sold,
    sum(gross_revenue_sar) as gross_revenue_sar,
    sum(discount_sar) as discount_sar,
    sum(refund_sar) as refund_sar,
    sum(net_revenue_sar) as net_revenue_sar,
    sum(cost_sar) as cost_sar,
    sum(ad_spend_sar) as ad_spend_sar
from {{ ref('stg_commerce_daily') }}
group by 1
