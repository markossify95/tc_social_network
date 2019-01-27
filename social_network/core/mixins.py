from rest_framework.exceptions import NotAuthenticated


class PasteUserMixin:
    def validate(self, attrs):
        attrs['user'] = self.context.get('request').user

        if attrs['user'].is_anonymous:
            raise NotAuthenticated()
        return attrs
