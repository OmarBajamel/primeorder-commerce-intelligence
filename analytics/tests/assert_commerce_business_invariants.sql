select *
from {{ ref('stg_commerce_daily') }}
where not (
    abs(gross_revenue_sar - discount_sar - refund_sar - net_revenue_sar) < 0.01
)
