with doctors as (

    select distinct
        doctor_name
    from {{ ref('stg_health_patient') }}
    where doctor_name is not null

)

select
    {{ dbt_utils.generate_surrogate_key([
        'doctor_name'
    ]) }} as doctor_key,

    doctor_name

from doctors