select
    activity_date,
    salla_purchases,
    ga4_purchases,
    salla_revenue_sar,
    ga4_revenue_sar,
    transaction_variance_rate,
    revenue_variance_rate,
    case when transaction_variance_rate <= 0.10 and revenue_variance_rate <= 0.10 then true else false end as within_tolerance
from {{ ref('int_source_comparison') }}
