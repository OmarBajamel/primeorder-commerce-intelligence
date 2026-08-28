with duplicate_transactions as (
    select sum(extra_rows) as affected_rows
    from (
        select count(*) - 1 as extra_rows
        from {{ ref('stg_orders') }} group by tracking_transaction_id having count(*) > 1
    )
),
unknown_products as (
    select count(*) as affected_rows from {{ ref('int_orders_enriched') }} where not is_product_mapped
),
event_parameters as (
    select sum(case when least(transaction_id_parameter_completeness, currency_parameter_completeness, value_parameter_completeness, items_parameter_completeness, item_id_parameter_completeness, item_name_parameter_completeness, item_category_parameter_completeness, price_parameter_completeness, quantity_parameter_completeness) < 1 then 1 else 0 end) as affected_rows,
           min(least(transaction_id_parameter_completeness, currency_parameter_completeness, value_parameter_completeness, items_parameter_completeness, item_id_parameter_completeness, item_name_parameter_completeness, item_category_parameter_completeness, price_parameter_completeness, quantity_parameter_completeness)) as metric_value
    from {{ ref('int_event_quality') }}
),
consent_coverage as (
    select
        sum(case when consent_state_coverage < 0.95 then 1 else 0 end) as affected_rows,
        min(consent_state_coverage) as metric_value
    from {{ ref('int_event_quality') }}
),
freshness as (
    select date_diff('day', max(search_date), date '2025-12-31') as affected_rows from {{ ref('stg_search_console') }}
),
reconciliation as (
    select sum(case when transaction_variance_rate > 0.10 or revenue_variance_rate > 0.10 then 1 else 0 end) as affected_rows,
           max(greatest(transaction_variance_rate, revenue_variance_rate)) as metric_value
    from {{ ref('int_source_comparison') }}
)
select 'duplicate_transactions' as check_id, 'high' as severity, affected_rows::double / (select count(*) from {{ ref('stg_orders') }}) as metric_value, 0.0 as threshold, affected_rows, case when affected_rows = 0 then 'pass' else 'warning' end as status from duplicate_transactions
union all
select 'unknown_products', 'high', affected_rows::double / (select count(*) from {{ ref('stg_order_items') }}), 0.0, affected_rows, case when affected_rows = 0 then 'pass' else 'warning' end from unknown_products
union all
select 'event_parameter_completeness', 'medium', metric_value, 1.0, affected_rows, case when metric_value >= 1 then 'pass' else 'warning' end from event_parameters
union all
select 'search_freshness_days', 'medium', affected_rows::double, 7.0, affected_rows, case when affected_rows <= 7 then 'pass' else 'warning' end from freshness
union all
select 'daily_reconciliation', 'medium', metric_value, 0.10, affected_rows, case when affected_rows = 0 then 'pass' else 'warning' end from reconciliation
union all
select 'consent_state_coverage', 'low', metric_value, 0.95, affected_rows, case when affected_rows = 0 then 'pass' else 'warning' end from consent_coverage
