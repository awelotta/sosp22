# Discord tagger Bot

Discord bot that provides commands to tag messages and search messages by tag.

## available tags

`!tag [MSG] [TAGS]`

[MSG] is the message. It should be referred to using one of three formats:
  1. [channel ID]-[message ID]
  2. message ID (the current channel is assumed to be the channel of the message)
  3. message URL

More information can be found here: https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.PartialMessageConverter
[TAGS] is the tag(s). They are space separated.

`!untag [MSG] [TAGS]`

This is the exact opposite of the `!tag` command. If you attempt to untag a tag that the message isn't tagged with, the tag will be ignored.

`!clean`

This removes from the internal database, any tags that have no associated messages, i.e. as a result of untagging.

`!alltags`

This displays all the tags and their usage frequencies.

`!msgtags [MSG]`

This displays all the tags on a message, in the format as with the `!tag` command. Does not display their usage frequences.

`!search [TAGS]`

`[TAGS]` is the list of tags. This displays a list of URLs to messages satisfying the list of tags. In order to satisfy, a message must have all the tags, i.e. the tags are ANDed aka INTERSECTed. However, if a tag is not in the internal database (e.g. after calling `!clean`), that tag will be ignored. E.g. if `foo` is a tag not in the internal database, and `bar` is a tag in the internal database, then `!search foo bar` is equivalent to `!search bar`.