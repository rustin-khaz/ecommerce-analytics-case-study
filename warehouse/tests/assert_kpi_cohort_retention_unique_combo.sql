-- dbt singular test: passes when this returns zero rows
select cohort_month, months_since_first_order, count(*)
from {{ ref('kpi_cohort_retention') }}
group by 1, 2
having count(*) > 1
