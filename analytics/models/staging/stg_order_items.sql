select
    cast(order_id as varchar) as order_id,
    cast(order_date as date) as order_date,
    cast(product_id as varchar) as product_id,
    cast(quantity as bigint) as quantity,
    cast(item_revenue_sar as decimal(18, 2)) as item_revenue_sar,
    cast(item_cost_sar as decimal(18, 2)) as item_cost_sar,
    cast(discount_sar as decimal(18, 2)) as discount_sar
from {{ ref('order_items') }}
