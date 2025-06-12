from rest_framework.serializers import ValidationError

def validate_image_size(image, max_size=5 * 1024 * 1024):
    """
    Validates the size of the uploaded image.
    
    :param image: The image file to validate.
    :param max_size: Maximum allowed size in bytes (default is 5MB).
    :raises ValidationError: If the image size exceeds the maximum allowed size.
    """
    if image.size > max_size:
        raise ValidationError(f"Image size should not exceed {max_size / (1024 * 1024)} MB.")
    return image
def validate_image_format(image, allowed_formats=None):
    """
    Validates the format of the uploaded image.
    """
    if allowed_formats is None:
        allowed_formats = ['image/jpeg', 'image/png', 'image/gif']
    if image.content_type not in allowed_formats:
        raise ValidationError(f"Unsupported image format. Allowed formats are: {', '.join(allowed_formats)}.")
    return image
def validate_image(image, max_size=5 * 1024 * 1024, allowed_formats=None):
    """
    Validates both the size and format of the uploaded image.
    """
    validate_image_size(image, max_size)
    validate_image_format(image, allowed_formats)
    return image

def validate_confirm_password(password, password2):

    """
    Validates that the two passwords match.
    
    :param password: The original password.
    :param password2: The confirmation password.
    :raises ValidationError: If the passwords do not match.
    """
    if password != password2:
        raise ValidationError("Passwords do not match.")
    return password
def validate_email_uniqueness(email, user_model):
    """
    Validates that the email is unique in the user model.
    :param email: The email to validate.
    :param user_model: The user model to check against.
    """
    if user_model.objects.filter(email=email).exists():
        raise ValidationError("Email already exists.")
    return email
