from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for email verification / account activation.

    Inherits Django's built-in PasswordResetTokenGenerator
    to create secure, time-sensitive tokens.
    """

    def _make_hash_value(self, user, timestamp):
        """
        Defines the data used to generate the token hash.

        If ANY of these values change, the token becomes invalid.
        """

        return (
            str(user.pk) +          # Unique user identifier
            str(timestamp) +        # Time-based component (for expiry)
            str(user.is_active)     # Invalidates token after activation
        )


# Create a reusable instance of the token generator
user_token_generator = UserVerificationTokenGenerator()
