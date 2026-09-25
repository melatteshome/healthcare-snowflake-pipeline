    {{
        config(
            materialized= 'view',
        )
    }}


with source as (

    select *
    from {{ source('healthcare', 'hospital_patients') }}

),

parsed as (

    select
        raw_data:"Name"::string                    as patient_name,
        try_to_number(raw_data:"Age"::string)      as age,
        raw_data:"Gender"::string                  as gender,
        raw_data:"Blood Type"::string              as blood_type,
        raw_data:"Medical Condition"::string       as medical_condition,
        try_to_date(raw_data:"Date of Admission"::string) as admission_date,
        raw_data:"Doctor"::string                  as doctor_name,
        raw_data:"Hospital"::string                as hospital_name,
        raw_data:"Insurance Provider"::string      as insurance_provider,
        raw_data:"Billing Amount"::number(12, 2)   as billing_amount,
        raw_data:"Room Number"::integer            as room_number,
        raw_data:"Admission Type"::string          as admission_type,
        try_to_date(raw_data:"Discharge Date"::string) as discharge_date,
        raw_data:"Medication"::string  
                    as medication,
        raw_data:"Test Results"::string            as test_results,

        source_file,
        loaded_at

    from source

)

select *
from parsed