def check_eye_contact(duration=3):
    import cv2
    import mediapipe as mp
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    mp_face_mesh = mp.solutions.face_mesh

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return 0

    frames = 0
    eye_contact_frames = 0

    with mp_face_mesh.FaceMesh(refine_landmarks=True) as face_mesh:
        while frames < duration * 3:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = face_mesh.process(rgb)

            if result.multi_face_landmarks:
                eye_contact_frames += 1

            frames += 1

    cap.release()

    if frames == 0:
        return 0

    return round((eye_contact_frames / frames) * 10, 2)