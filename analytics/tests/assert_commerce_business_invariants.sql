select *
from {{ ref('stg_commerce_daily') }}
where not (
    sessions >= users
    and sessions >= product_views
    and product_views >= add_to_carts
    and add_to_carts >= begin_checkouts
    and begin_checkouts >= purchases
    and abs(gross_revenue_sar - discount_sar - refund_sar - net_revenue_sar) < 0.01
)
