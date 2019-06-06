# -*- coding: utf-8 -*-

import requests
from db import StatDataBase
import os

database_address = 'social_stat.db'

vk_groups = (
    'rambler',
    'ramblermail',
    'horoscopesrambler',
    'championat',
    'championat.auto',
    'championat_cybersport',
    'livejournal',
    'afisha',
)


def get_vk_subs(group,
                token=os.environ.get('VK_TOKEN'),
                api_version='5.95',
                api_url='https://api.vk.com/',
                method='groups.getMembers',
                ):
    """Return subs_count from VK group by group id. Or 0 if error."""
    url = '{0}method/{1}?group_id={2}&access_token={3}&v={4}'.format(
        api_url,
        method,
        group,
        token,
        api_version,
    )
    result = requests.get(url)
    try:
        subs_count = result.json()['response']['count']
    except KeyError:
        subs_count = 0
    return subs_count


def main():
    """Get subs count for vk group and insert it into DB."""
    db = StatDataBase(database_address)
    db.db_init()

    for group in vk_groups:
        group_id = db.db_check_group(group)
        if not group_id:
            db.db_insert_group(group)
            group_id = db.db_check_group(group)
        subs_count = get_vk_subs(group)
        db.db_insert_subs(group_id, subs_count)


if __name__ == '__main__':
    main()
