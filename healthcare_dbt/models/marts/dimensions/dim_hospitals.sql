with hospitals as (

    select distinct
        hospital_name
    from {{ ref('stg_health_patient') }}
    where hospital_name is not null

)

select
    {{ dbt_utils.generate_surrogate_key([
        'hospital_name'
    ]) }} as hospital_key,

    hospital_name

from hospitals