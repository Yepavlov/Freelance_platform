import os


def documentation_upload(instance, filename):
    client_id = instance.client_profile_id
    _, ext = os.path.splitext(filename)
    return f"proposal/documentation/freelancer_{client_id}/{filename}"
