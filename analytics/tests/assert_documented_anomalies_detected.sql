with expected(check_id, affected_rows) as (
    values ('duplicate_transactions', 1), ('unknown_products', 1),
           ('event_parameter_completeness', 1), ('search_freshness_days', 11),
           ('daily_reconciliation', 5), ('consent_state_coverage', 11)
), compared as (
    select coalesce(expected.check_id, quality.check_id) as check_id,
           expected.affected_rows as expected_rows,
           quality.affected_rows as actual_rows,
           quality.status
    from expected
    full outer join {{ ref('mart_data_quality') }} quality using (check_id)
)
select * from compared
where expected_rows is null or actual_rows is null or actual_rows <> expected_rows or status <> 'warning'
