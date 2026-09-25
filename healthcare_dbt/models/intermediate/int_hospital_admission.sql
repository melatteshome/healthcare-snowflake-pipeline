    {{ config(
        materialized='view'
    ) }}

with patients as (

    select *
    from {{ ref('stg_health_patient') }}

),

final as (

    select
        *,

        -- Number of days the patient stayed
        datediff(
            'day',
            admission_date,
            discharge_date
        ) as length_of_stay_days,

        -- Simple billing classification
        case
            when billing_amount < 0 then 'invalid'
            when billing_amount = 0 then 'no_charge'
            else 'billable'
        end as billing_status

    from patients

)

select *
from final