select
    cast(date as date) as diagnostic_date,
    cast(product_id as varchar) as product_id,
    cast(destination as varchar) as destination,
    lower(cast(status as varchar)) as status,
    cast(issue_code as varchar) as issue_code,
    cast(affected_items as bigint) as affected_items
from {{ ref('merchant_diagnostics') }}
