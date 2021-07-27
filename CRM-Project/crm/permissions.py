from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class AccesUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.profile.is_consultant_specialist or
            self.request.user.profile.is_repair_specialist or
            self.request.user.profile.is_service_specialist or
            self.request.user.is_staff
            )
