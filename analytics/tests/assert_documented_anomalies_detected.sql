with required(check_id) as (
    values ('duplicate_transactions'), ('unknown_products'), ('event_parameter_completeness'),
           ('search_freshness_days'), ('daily_reconciliation'), ('consent_state_coverage')
)
select required.check_id
from required
left join {{ ref('mart_data_quality') }} quality using (check_id)
where quality.check_id is null or quality.status <> 'warning' or quality.affected_rows <= 0
