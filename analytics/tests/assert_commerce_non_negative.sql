select *
from {{ ref('stg_commerce_daily') }}
where sessions < 0 or users < 0 or product_views < 0 or add_to_carts < 0
   or begin_checkouts < 0 or purchases < 0 or units_sold < 0
   or gross_revenue_sar < 0 or discount_sar < 0 or refund_sar < 0
   or net_revenue_sar < 0 or cost_sar < 0 or ad_spend_sar < 0
