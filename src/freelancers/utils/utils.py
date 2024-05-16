import os


def documentation_upload(instance, filename):
    freelancer_id = instance.freelancer_profile_id
    _, ext = os.path.splitext(filename)
    return f"proposal/documentation/freelancer_{freelancer_id}/{filename}"
