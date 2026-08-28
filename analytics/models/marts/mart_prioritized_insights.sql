with metrics as (
    select
        (select affected_rows from {{ ref('mart_data_quality') }} where check_id = 'duplicate_transactions') as duplicate_rows,
        (select affected_rows from {{ ref('mart_data_quality') }} where check_id = 'search_freshness_days') as stale_days,
        (select 1 - sum(purchases)::double / nullif(sum(begin_checkouts), 0) from {{ ref('int_daily_commerce') }}) as checkout_abandonment
)
select 'INS-001' as insight_id, 1 as priority, 'measurement' as area, 'Resolve duplicate transaction tracking' as title,
       concat(duplicate_rows, ' duplicate synthetic tracking row detected') as evidence,
       'high' as confidence, 'Deduplicate purchase events by transaction_id before attribution.' as recommended_action from metrics
union all
select 'INS-002', 2, 'funnel', 'Investigate checkout abandonment', concat(round(checkout_abandonment * 100, 1), '% checkout-to-purchase abandonment'),
       'medium', 'Segment checkout friction by device and payment method, then test one change.' from metrics
union all
select 'INS-003', 3, 'seo', 'Refresh Search Console ingestion', concat(stale_days, ' days stale at fixture end'),
       'high', 'Restore daily extraction and alert when freshness exceeds seven days.' from metrics
