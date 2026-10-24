import streamlit as st
import time

from database import (
    create_database,
    register_user,
    get_user,
    verify_password,
)

from otp import (
    generate_otp,
    send_otp,
)

from face import (
    save_registered_face,
    verify_face,
)


# ===================================================
# PAGE CONFIGURATION
# ===================================================

st.set_page_config(
    page_title="Three-Level Authentication System",
    page_icon="🔐",
    layout="centered",
)


# ===================================================
# CREATE DATABASE
# ===================================================

create_database()


# ===================================================
# SESSION STATE
# ===================================================

default_states = {
    "level1": False,
    "level2": False,
    "level3": False,
    "authenticated": False,

    "user_id": None,
    "username": None,
    "phone": None,

    "otp": None,
    "otp_expiry": None,
    "otp_sent": False,
}

for key, value in default_states.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ===================================================
# RESET AUTHENTICATION
# ===================================================

def reset_authentication():

    st.session_state.level1 = False
    st.session_state.level2 = False
    st.session_state.level3 = False

    st.session_state.authenticated = False

    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.phone = None

    st.session_state.otp = None
    st.session_state.otp_expiry = None
    st.session_state.otp_sent = False


# ===================================================
# TITLE
# ===================================================

st.title("🔐 Three-Level Authentication System")

st.caption(
    "Password Authentication → Phone OTP → Face Verification"
)

st.divider()


# ===================================================
# AUTHENTICATED DASHBOARD
# ===================================================

if st.session_state.authenticated:

    st.success("🎉 Authentication Successful!")

    st.header("🎓 Secure Portal")

    st.write(
        f"Welcome, **{st.session_state.username}**!"
    )

    st.subheader("Authentication Status")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.success("🔑 Password")
        st.write("Verified")

    with col2:

        st.success("📱 Phone OTP")
        st.write("Verified")

    with col3:

        st.success("👤 Face")
        st.write("Verified")

    st.divider()

    st.subheader("📊 Dashboard")

    col1, col2 = st.columns(2)

    with col1:

        st.info("👤 Profile")

        st.write(
            f"Username: {st.session_state.username}"
        )

        st.write(
            f"Phone: {st.session_state.phone}"
        )

    with col2:

        st.info("🔒 Security")

        st.write(
            "Three-Level Authentication"
        )

        st.write(
            "Status: Active"
        )

    st.divider()

    st.subheader("Portal Services")

    col1, col2 = st.columns(2)

    with col1:

        st.button(
            "📚 Courses",
            use_container_width=True
        )

        st.button(
            "📊 Results",
            use_container_width=True
        )

    with col2:

        st.button(
            "📅 Attendance",
            use_container_width=True
        )

        st.button(
            "💰 Fees",
            use_container_width=True
        )

    st.divider()

    if st.button(
        "🚪 Logout",
        type="primary",
        use_container_width=True
    ):

        reset_authentication()

        st.success(
            "Logged out successfully."
        )

        st.rerun()


# ===================================================
# NOT AUTHENTICATED
# ===================================================

else:

    # =================================================
    # SIDEBAR
    # =================================================

    st.sidebar.title(
        "🔐 Authentication"
    )

    menu = st.sidebar.radio(
        "Select Option",
        [
            "Login",
            "Register"
        ]
    )


    # =================================================
    # REGISTRATION
    # =================================================

    if menu == "Register":

        st.header(
            "📝 User Registration"
        )

        st.write(
            "Create your account before using "
            "the authentication system."
        )


        # ---------------------------------------------
        # USERNAME
        # ---------------------------------------------

        username = st.text_input(
            "Username",
            key="register_username"
        )


        # ---------------------------------------------
        # PHONE NUMBER
        # ---------------------------------------------

        phone = st.text_input(
            "Phone Number",
            key="register_phone",
            placeholder="Enter 10-digit phone number"
        )


        # ---------------------------------------------
        # PASSWORD
        # ---------------------------------------------

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )


        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm_password"
        )


        # ---------------------------------------------
        # FACE REGISTRATION
        # ---------------------------------------------

        st.subheader(
            "📷 Face Registration"
        )

        st.write(
            "Look directly at the camera and "
            "capture a clear image."
        )

        registered_face = st.camera_input(
            "Capture Face",
            key="registration_camera"
        )


        # ---------------------------------------------
        # CREATE ACCOUNT
        # ---------------------------------------------

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True
        ):

            # -----------------------------------------
            # VALIDATION
            # -----------------------------------------

            if not username:

                st.warning(
                    "Please enter a username."
                )

            elif not phone:

                st.warning(
                    "Please enter your phone number."
                )

            elif not phone.isdigit():

                st.warning(
                    "Phone number must contain "
                    "numbers only."
                )

            elif len(phone) != 10:

                st.warning(
                    "Please enter a valid "
                    "10-digit phone number."
                )

            elif not password:

                st.warning(
                    "Please enter a password."
                )

            elif len(password) < 6:

                st.warning(
                    "Password must contain at "
                    "least 6 characters."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif registered_face is None:

                st.warning(
                    "Please capture your face."
                )

            else:

                try:

                    # ---------------------------------
                    # REGISTER USER
                    # ---------------------------------

                    user_id = register_user(
                        username,
                        phone,
                        password
                    )


                    # ---------------------------------
                    # SAVE REGISTERED FACE
                    # ---------------------------------

                    save_registered_face(
                        user_id,
                        registered_face
                    )


                    st.success(
                        "✅ Registration successful!"
                    )

                    st.info(
                        "Select Login from the "
                        "sidebar to continue."
                    )

                except Exception as e:

                    st.error(
                        f"Registration failed: {e}"
                    )


    # =================================================
    # LOGIN
    # =================================================

    elif menu == "Login":


        # =================================================
        # LEVEL 1
        # PASSWORD AUTHENTICATION
        # =================================================

        if not st.session_state.level1:

            st.header(
                "🔑 Level 1: Password Authentication"
            )

            st.write(
                "Enter your registered username "
                "and password."
            )


            login_username = st.text_input(
                "Username",
                key="login_username"
            )


            login_password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )


            if st.button(
                "Login",
                type="primary",
                use_container_width=True
            ):

                if not login_username:

                    st.warning(
                        "Please enter your username."
                    )

                elif not login_password:

                    st.warning(
                        "Please enter your password."
                    )

                else:

                    user = get_user(
                        login_username
                    )


                    if user is None:

                        st.error(
                            "❌ Invalid username "
                            "or password."
                        )


                    elif verify_password(
                        login_password,
                        user["password"]
                    ):

                        # -----------------------------
                        # SAVE USER INFORMATION
                        # -----------------------------

                        st.session_state.user_id = (
                            user["id"]
                        )

                        st.session_state.username = (
                            user["username"]
                        )

                        st.session_state.phone = (
                            user["phone"]
                        )


                        # -----------------------------
                        # LEVEL 1 PASSED
                        # -----------------------------

                        st.session_state.level1 = True

                        st.success(
                            "✅ Level 1 Passed!"
                        )

                        st.rerun()


                    else:

                        st.error(
                            "❌ Invalid username "
                            "or password."
                        )


        # =================================================
        # LEVEL 2
        # PHONE OTP VERIFICATION
        # =================================================

        elif (
            st.session_state.level1
            and not st.session_state.level2
        ):

            st.header(
                "📱 Level 2: Phone OTP Verification"
            )

            st.success(
                "✅ Level 1: Password Verified"
            )

            st.write(
                "Generate an OTP for your "
                "registered phone number."
            )

            st.write(
                f"Phone Number: "
                f"**{st.session_state.phone}**"
            )


            # ---------------------------------------------
            # SEND OTP
            # ---------------------------------------------

            if not st.session_state.otp_sent:

                if st.button(
                    "📨 Send OTP",
                    type="primary",
                    use_container_width=True
                ):

                    try:

                        # Generate OTP
                        otp = generate_otp()


                        # Send/display OTP
                        send_otp(
                            st.session_state.phone,
                            otp
                        )


                        # Store OTP
                        st.session_state.otp = otp


                        # OTP expires after 5 minutes
                        st.session_state.otp_expiry = (
                            time.time() + 300
                        )


                        st.session_state.otp_sent = True


                        st.success(
                            "📱 OTP generated successfully!"
                        )


                        st.rerun()


                    except Exception as e:

                        st.error(
                            f"Unable to generate OTP: {e}"
                        )


            # ---------------------------------------------
            # VERIFY OTP
            # ---------------------------------------------

            if st.session_state.otp_sent:

                st.info(
                    "For the test version, "
                    "check the VS Code terminal "
                    "for your OTP."
                )


                entered_otp = st.text_input(
                    "Enter 6-Digit OTP",
                    max_chars=6,
                    key="entered_phone_otp"
                )


                if st.button(
                    "Verify OTP",
                    type="primary",
                    use_container_width=True
                ):

                    if not entered_otp:

                        st.warning(
                            "Please enter the OTP."
                        )


                    elif (
                        time.time()
                        > st.session_state.otp_expiry
                    ):

                        st.error(
                            "❌ OTP expired. "
                            "Please request a new OTP."
                        )

                        st.session_state.otp = None

                        st.session_state.otp_expiry = (
                            None
                        )

                        st.session_state.otp_sent = (
                            False
                        )

                        st.rerun()


                    elif entered_otp == (
                        st.session_state.otp
                    ):

                        # -----------------------------
                        # LEVEL 2 PASSED
                        # -----------------------------

                        st.session_state.level2 = True


                        # Delete OTP
                        st.session_state.otp = None

                        st.session_state.otp_expiry = (
                            None
                        )

                        st.session_state.otp_sent = (
                            False
                        )


                        st.success(
                            "✅ Level 2 Passed!"
                        )


                        st.rerun()


                    else:

                        st.error(
                            "❌ Incorrect OTP. "
                            "Please try again."
                        )


                # -----------------------------------------
                # RESEND OTP
                # -----------------------------------------

                if st.button(
                    "🔄 Resend OTP",
                    use_container_width=True
                ):

                    try:

                        # Generate new OTP
                        new_otp = generate_otp()


                        # Send/display new OTP
                        send_otp(
                            st.session_state.phone,
                            new_otp
                        )


                        # Replace old OTP
                        st.session_state.otp = new_otp


                        # Reset expiry
                        st.session_state.otp_expiry = (
                            time.time() + 300
                        )


                        st.success(
                            "📱 New OTP generated!"
                        )


                        st.info(
                            "Check the VS Code terminal "
                            "for the new OTP."
                        )


                    except Exception as e:

                        st.error(
                            f"Unable to resend OTP: {e}"
                        )


        # =================================================
        # LEVEL 3
        # FACE VERIFICATION
        # =================================================

        elif (
            st.session_state.level1
            and st.session_state.level2
            and not st.session_state.level3
        ):

            st.header(
                "👤 Level 3: Face Verification"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.success(
                    "✅ Password Verified"
                )


            with col2:

                st.success(
                    "✅ Phone OTP Verified"
                )


            st.write(
                "Capture a clear image "
                "of your face."
            )


            st.info(
                "Look directly at the camera "
                "and make sure there is "
                "enough light."
            )


            current_face = st.camera_input(
                "📷 Capture Face for Verification",
                key="verification_camera"
            )


            if current_face is not None:

                if st.button(
                    "👤 Verify Face",
                    type="primary",
                    use_container_width=True
                ):

                    try:

                        matched = verify_face(
                            st.session_state.user_id,
                            current_face
                        )


                        if matched:

                            st.session_state.level3 = (
                                True
                            )

                            st.session_state.authenticated = (
                                True
                            )


                            st.success(
                                "✅ Face Verified!"
                            )

                            st.success(
                                "🔓 Access Granted!"
                            )

                            st.rerun()


                        else:

                            st.error(
                                "❌ Face verification "
                                "failed."
                            )

                            st.warning(
                                "Please capture your "
                                "face again."
                            )


                    except Exception as e:

                        st.error(
                            f"Face verification error: {e}"
                        )


        # =================================================
        # FALLBACK
        # =================================================

        else:

            st.error(
                "Authentication state error."
            )

            if st.button(
                "Restart Login"
            ):

                reset_authentication()

                st.rerun()


# ===================================================
# FOOTER
# ===================================================

st.divider()

st.caption(
    "🔐 Python-Based Three-Level Authentication System"
)