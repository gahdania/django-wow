# Django WoW Website


## Installation

Windows, OS X & Linux:

    pip install battlenet_client

## Clone
Clone the latest version: https://gitlab.com/battlenet1/battlenet-client.git

## Usage Example
    # Simplist Form
    # <client_id> and <client_secret> found in your battle.net developer account
    > from battlenet_client import wow
    > client = wow.WoWClient(<region>, client_id=<client_id>, client_secret=<client_secret>
    > client.playable_class.playable_class(<locale>, <class id>)
    {'_links': {'self': {'href': 'https://us.api.blizzard.com/data/wow/playable-class/7?namespace=static-9.1.5_40764-us'}}, 'id': 7, 'name': 'Shaman', 'gender_name': {'male': 'Shaman', 'female': 'Shaman'}, 'power_type': {'key': {'href': 'https://us.api.blizzard.com/data/wow/power-type/0?namespace=static-9.1.5_40764-us'}, 'name': 'Mana', 'id': 0}, 'specializations': [{'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/262?namespace=static-9.1.5_40764-us'}, 'name': 'Elemental', 'id': 262}, {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/263?namespace=static-9.1.5_40764-us'}, 'name': 'Enhancement', 'id': 263}, {'key': {'href': 'https://us.api.blizzard.com/data/wow/playable-specialization/264?namespace=static-9.1.5_40764-us'}, 'name': 'Restoration', 'id': 264}], 'media': {'key': {'href': 'https://us.api.blizzard.com/data/wow/media/playable-class/7?namespace=static-9.1.5_40764-us'}, 'id': 7}, 'pvp_talent_slots': {'href': 'https://us.api.blizzard.com/data/wow/playable-class/7/pvp-talent-slots?namespace=static-9.1.5_40764-us'}}

For more information, please the [wiki][wiki]

Note: This package is a dependency of my other [Battle.net REST API packages](https://gitlab.com/battlenet1)

## Release History
Please change log for complete history

## Meta

David "Gahd" Couples – [@gahdania][twitter] [Twitch][twitch] – gahdania@gahd.io

Distributed under the GPL v3+ license. See ``LICENSE`` for more information.

[Battle.net Client on Gitlab][gitlab]

## Contributing

1. [Fork it][fork]
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[wiki]: https://gitlab.com/battlenet1/battlenet-client/-/wikis/home
[twitter]: https://twitter.com/gahdania
[twitch]: https://www.twitch.tv/gahd
[gitlab]: https://gitlab.com/battlenet1/battlenet-client
[fork]: https://gitlab.com/battlenet1/battlenet-client/-/forks/new
