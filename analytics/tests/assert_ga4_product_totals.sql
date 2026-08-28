with daily as (
    select activity_date, device, channel,
           sum(sessions) as sessions, sum(users) as active_user_days,
           sum(product_views) as product_views, sum(add_to_carts) as add_to_carts,
           sum(begin_checkouts) as begin_checkouts, sum(purchases) as tracked_purchases
    from {{ ref('stg_ga4_daily') }} group by 1, 2, 3
), product as (
    select activity_date, device, channel,
           sum(sessions) as sessions, sum(active_user_days) as active_user_days,
           sum(product_views) as product_views, sum(add_to_carts) as add_to_carts,
           sum(begin_checkouts) as begin_checkouts, sum(tracked_purchases) as tracked_purchases
    from {{ ref('stg_ga4_product_daily') }} group by 1, 2, 3
)
select daily.activity_date
from daily full outer join product using (activity_date, device, channel)
where daily.sessions <> product.sessions
   or daily.active_user_days <> product.active_user_days
   or daily.product_views <> product.product_views
   or daily.add_to_carts <> product.add_to_carts
   or daily.begin_checkouts <> product.begin_checkouts
   or daily.tracked_purchases <> product.tracked_purchases
