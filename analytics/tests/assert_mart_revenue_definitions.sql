with executive as (
    select
        sum(net_revenue_sar) as net_revenue_sar,
        sum(gross_margin_sar) as gross_margin_sar,
        sum(net_revenue_sar) / nullif(sum(completed_orders), 0) as calculated_aov,
        sum(average_order_value_sar * completed_orders) / nullif(sum(completed_orders), 0) as published_weighted_aov
    from {{ ref('mart_executive_daily') }}
), products as (
    select sum(revenue_sar) as net_revenue_sar, sum(gross_margin_sar) as gross_margin_sar
    from {{ ref('mart_product_performance') }}
)
select 1
from executive cross join products
where abs(executive.net_revenue_sar - products.net_revenue_sar) >= 0.01
   or abs(executive.gross_margin_sar - products.gross_margin_sar) >= 0.01
   or abs(executive.calculated_aov - executive.published_weighted_aov) >= 0.000001
