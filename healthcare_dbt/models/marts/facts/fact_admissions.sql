with admissions as (

    select *
    from {{ ref('int_hospital_admission') }}

),

final as (

    select
        p.patient_key,
        d.doctor_key,
        h.hospital_key,

        a.admission_date,
        a.discharge_date,
        a.admission_type,
        a.medical_condition,
        a.medication,
        a.insurance_provider,
        a.room_number,
        a.test_results,

        a.billing_amount,
        a.length_of_stay_days,

        a.source_file,
        a.loaded_at

    from admissions a

    left join {{ ref('dim_patient') }} p
        on a.patient_name = p.patient_name
        and a.age = p.age
        and a.gender = p.gender
        and a.blood_type = p.blood_type

    left join {{ ref('dim_doctor') }} d
        on a.doctor_name = d.doctor_name

    left join {{ ref('dim_hospital') }} h
        on a.hospital_name = h.hospital_name

)

select *
from final