from django.db import models


class OrgQuerySet(models.QuerySet):
    def for_org(self, org):
        return self.filter(organization=org)
