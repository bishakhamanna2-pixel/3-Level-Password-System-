import secrets


def generate_otp():
    """
    Generate a secure random 6-digit OTP.
    """

    return str(secrets.randbelow(900000) + 100000)


def send_otp(phone_number, otp):
    """
    Simulated SMS OTP for project testing.

    Later this function can be replaced
    with a real SMS API.
    """

    print("--------------------------------")
    print("SMS OTP")
    print("--------------------------------")
    print("Phone Number:", phone_number)
    print("OTP:", otp)
    print("--------------------------------")

    return True


if __name__ == "__main__":

    phone = input("Enter phone number: ")

    otp = generate_otp()

    send_otp(phone, otp)