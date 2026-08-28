select *
from {{ ref('stg_commerce_daily') }}
where purchases < 0 or units_sold < 0
   or gross_revenue_sar < 0 or discount_sar < 0 or refund_sar < 0
   or net_revenue_sar < 0 or cost_sar < 0
