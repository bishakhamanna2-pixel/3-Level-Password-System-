#Face registration and face verification

import os
import cv2
import numpy as np

from database import update_face_path, get_user_by_id


# ---------------------------------------------------
# FACE STORAGE FOLDER
# ---------------------------------------------------

FACE_FOLDER = "faces"

os.makedirs(FACE_FOLDER, exist_ok=True)


# ---------------------------------------------------
# LOAD STREAMLIT CAMERA IMAGE
# ---------------------------------------------------

def camera_image_to_cv2(uploaded_image):
    """
    Convert an image returned by st.camera_input()
    into an OpenCV image.
    """

    if uploaded_image is None:
        return None

    image_bytes = uploaded_image.getvalue()

    numpy_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        numpy_array,
        cv2.IMREAD_COLOR
    )

    return image


# ---------------------------------------------------
# LOAD FACE DETECTOR
# ---------------------------------------------------

def get_face_detector():
    """
    Load OpenCV Haar Cascade face detector.
    """

    cascade_path = os.path.join(
        cv2.data.haarcascades,
        "haarcascade_frontalface_default.xml"
    )

    detector = cv2.CascadeClassifier(cascade_path)

    if detector.empty():
        raise ValueError(
            "Unable to load OpenCV face detector."
        )

    return detector


# ---------------------------------------------------
# EXTRACT FACE
# ---------------------------------------------------

def extract_face(image):
    """
    Detect a face and return the cropped,
    grayscale face.

    Returns None when no face is detected.
    """

    if image is None:
        return None

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    detector = get_face_detector()

    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    if len(faces) == 0:
        return None

    # Use the largest detected face
    x, y, w, h = max(
        faces,
        key=lambda face: face[2] * face[3]
    )

    face = gray[
        y:y + h,
        x:x + w
    ]

    # Give every face the same dimensions
    face = cv2.resize(
        face,
        (200, 200)
    )

    # Improve contrast
    face = cv2.equalizeHist(face)

    return face


# ---------------------------------------------------
# SAVE REGISTERED FACE
# ---------------------------------------------------

def save_registered_face(user_id, uploaded_image):
    """
    Save the face captured during registration.

    Returns the saved image path.
    """

    image = camera_image_to_cv2(uploaded_image)

    if image is None:
        raise ValueError(
            "Unable to read the captured image."
        )

    face = extract_face(image)

    if face is None:
        raise ValueError(
            "No face detected. Please capture "
            "a clear image of your face."
        )

    face_path = os.path.join(
        FACE_FOLDER,
        f"user_{user_id}.jpg"
    )

    success = cv2.imwrite(
        face_path,
        face
    )

    if not success:
        raise ValueError(
            "Unable to save registered face."
        )

    # Save path in SQLite
    update_face_path(
        user_id,
        face_path
    )

    return face_path


# ---------------------------------------------------
# VERIFY FACE
# ---------------------------------------------------

def verify_face(user_id, uploaded_image):
    """
    Compare the currently captured face with
    the face registered for the given user.

    Returns:
        True  -> face matched
        False -> face did not match
    """

    user = get_user_by_id(user_id)

    if user is None:
        raise ValueError(
            "User not found."
        )

    face_path = user["face_path"]

    if not face_path:
        raise ValueError(
            "No registered face found for this user."
        )

    if not os.path.exists(face_path):
        raise ValueError(
            "Registered face image is missing."
        )

    # -----------------------------------------------
    # LOAD REGISTERED FACE
    # -----------------------------------------------

    registered_face = cv2.imread(
        face_path,
        cv2.IMREAD_GRAYSCALE
    )

    if registered_face is None:
        raise ValueError(
            "Unable to load registered face."
        )

    registered_face = cv2.resize(
        registered_face,
        (200, 200)
    )

    # -----------------------------------------------
    # GET CURRENT FACE
    # -----------------------------------------------

    current_image = camera_image_to_cv2(
        uploaded_image
    )

    current_face = extract_face(
        current_image
    )

    if current_face is None:
        raise ValueError(
            "No face detected. Please look directly "
            "at the camera and try again."
        )

    # -----------------------------------------------
    # CREATE LBPH FACE RECOGNIZER
    # -----------------------------------------------

    try:
        recognizer = (
            cv2.face.LBPHFaceRecognizer_create()
        )

    except AttributeError:
        raise ValueError(
            "OpenCV face module is unavailable. "
            "Install opencv-contrib-python."
        )

    # -----------------------------------------------
    # TRAIN USING REGISTERED FACE
    # -----------------------------------------------

    recognizer.train(
        [registered_face],
        np.array([1])
    )

    # -----------------------------------------------
    # COMPARE CURRENT FACE
    # -----------------------------------------------

    label, confidence = recognizer.predict(
        current_face
    )

    print(
        "Face verification confidence:",
        confidence
    )

    # IMPORTANT:
    # With LBPH, LOWER distance is better.
    #
    # This is only a starting threshold for
    # this college-project prototype.
    threshold = 55

    if label == 1 and confidence < threshold:
        return True

    return False


# ---------------------------------------------------
# DIRECT TEST
# ---------------------------------------------------

if __name__ == "__main__":

    print("Face Authentication Module")
    print("--------------------------")
    print("Module loaded successfully.")