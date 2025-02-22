from rest_framework_simplejwt.tokens import RefreshToken


def generate_tokens(user)->tuple[str]:
    refresh = RefreshToken.for_user(user=user)
    access_token = refresh.access_token
    return(refresh, access_token)