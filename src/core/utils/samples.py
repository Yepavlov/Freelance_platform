from clients.utils.samples import sample_client_profile, sample_job
from core.models import BankingInformation, Payment
from core.utils.samples_for_location import sample_country
from freelancers.utils.samples import sample_freelancer_profile


def sample_payment(client_email: str, amount: float, method: str, **params):
    job = sample_job(
        user_email=client_email,
        title="Python dev",
        description="Creating a web application",
        hourly_rate=52.00,
        estimated_end_date="2024-09-25",
    )
    default = {
        "description": "Payment for contract 1",
        "job": job,
    }
    default.update(params)
    return Payment(
        amount=amount,
        method=method,
        **default,
    )


def sample_banking_information(
    account_holder_name: str,
    account_number: str,
    bank_name: str,
    country_name: str,
    currency: int,
    client_email=None,
    freelancer_email=None,
    **params
):
    default = {}
    country_instance = sample_country(country_name)

    if client_email:
        client = sample_client_profile(
            user_email=client_email,
        )
        default.update(
            {
                "client_profile": client,
                "country": country_instance,
            }
        )

    if freelancer_email:
        freelancer = sample_freelancer_profile(
            user_email=freelancer_email,
            position="Python developer",
            hourly_rate=25.00,
            sex=0,
        )
        default.update(
            {
                "freelancer_profile": freelancer,
                "country": country_instance,
            }
        )

    default.update(params)

    return BankingInformation(
        account_holder_name=account_holder_name,
        account_number=account_number,
        bank_name=bank_name,
        currency=currency,
        **default,
    )
