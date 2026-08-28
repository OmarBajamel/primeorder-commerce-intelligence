select 1
from {{ ref('mart_source_reconciliation') }}
having abs(sum(salla_purchases) - sum(ga4_purchases))::double / nullif(sum(salla_purchases), 0) > 0.10
    or abs(sum(salla_revenue_sar) - sum(ga4_revenue_sar)) / nullif(sum(salla_revenue_sar), 0) > 0.10
