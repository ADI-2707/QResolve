from slugify import slugify

from app.models import Organization
from app.repositories import OrganizationRepository


class OrganizationService:
    def __init__(
        self,
        repository: OrganizationRepository,
    ):
        self.repository = repository

    def create(
        self,
        name: str,
    ) -> Organization:

        slug = self._generate_unique_slug(
            name,
        )

        organization = Organization(
            name=name,
            slug=slug,
        )

        return self.repository.create(
            organization,
        )

    def get(
        self,
        organization_id: str,
    ) -> Organization | None:

        return self.repository.get_by_id(
            organization_id,
        )

    def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:

        return self.repository.get_by_slug(
            slug,
        )

    def list(self) -> list[Organization]:

        return self.repository.list()

    def _generate_unique_slug(
            self,
            organization_name: str,
    ) -> str:

        base_slug = slugify(
            organization_name,
        )

        if not base_slug:
            raise ValueError(
                "Organization name cannot generate a valid slug"
            )

        slug = base_slug

        counter = 2

        while self.repository.exists_by_slug(
                slug,
        ):
            slug = (
                f"{base_slug}-{counter}"
            )

            counter += 1

        return slug