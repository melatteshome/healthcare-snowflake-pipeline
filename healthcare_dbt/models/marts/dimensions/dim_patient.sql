with patients as (

    select
        patient_name,
        age,
        gender,
        blood_type

    from {{ ref('stg_health_patient') }}

),

final as (

    select
        {{ dbt_utils.generate_surrogate_key([
            'patient_name',
            'age',
            'gender',
            'blood_type'
        ]) }} as patient_key,

        patient_name,
        age,
        gender,
        blood_type

    from patients

)

select *
from final