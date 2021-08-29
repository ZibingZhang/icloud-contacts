from app import config
from app.contact import (
    Group,
)
from app.jobs import BaseJob


class SyncGroupsJob(BaseJob):
    def run(self, preview=True):
        existing_groups = self.client.groups()
        existing_group_names = map(lambda group: group.name, existing_groups)
        for group_def in config.GROUP_DEFINITIONS:
            satisfied_contact_ids = [
                contact.contact_id
                for contact in filter(group_def.condition, self.client.contacts())
            ]

            if group_def.name not in existing_group_names:
                print(f"Creating group: {group_def.name}")
                if not preview:
                    self.client.create_group(
                        Group(name=group_def.name, contact_ids=satisfied_contact_ids)
                    )
            else:
                existing_group = next(
                    filter(
                        lambda grp: grp.name == group_def.name,
                        existing_groups,
                    )
                )
                if set(existing_group.contact_ids) != set(satisfied_contact_ids):
                    print(f"Recreating group: {group_def.name}")
                    if not preview:
                        self.client.delete_group(existing_group)
                        self.client.create_group(
                            Group(
                                name=group_def.name, contact_ids=satisfied_contact_ids
                            )
                        )
