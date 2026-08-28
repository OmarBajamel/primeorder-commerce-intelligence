select 1
from (
    select sum(revenue_sar) as category_revenue from {{ ref('mart_category_performance') }}
) categories
cross join (
    select sum(revenue_sar) as product_revenue from {{ ref('mart_product_performance') }}
) products
where abs(categories.category_revenue - products.product_revenue) >= 0.01
