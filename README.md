# geobot
geobot for the fediverse (using mastodon API)

# security considerations

if you want to set this up, you'll need to store GeoGuessr session tokens on the system you're running this from. i am not a very responsible being, so please do the considerations on your own. hijacking your account using this is probably a possibility. from what i can tell, they do display your e-mail address in account settings, but not credit card information (that's probably stored with another service, even). 

# setting up
you'll need to have a few things first:
- a pro GeoGuessr account (~$3 a month, or $24 a year, practical to have one already)
- a bot account on a fedi instance with mastodon API support

first, you'll want to export your cookies from your browser. there are addons for this (e. g. https://github.com/rotemdan/ExportCookies, https://github.com/hrdl-github/cookies-txt). i have used the former, but only because i didn't know the the latter (which has been updated in the past 4 years) existed until now. lol. anyway, you should just export cookies from geoguessr website at most, for security reasons. see above for more security considerations. you'll need to edit both files: keys.py with the API token you have from mastodon ([this tool](https://takahashim.github.io/mastodon-access-token/) worked for me for generating one), and the main geobot.py file for any config lines in the beginning. what you'll certainly need to change are the instance URL, and the cookies file's name. you can also change whether you allow move, pan, zoom, the time limit, the map (the default is A Community World), and options surrounding the post (body - URL always goes at the end tho - and cw).

one thing i'd love to add is challenge summaries (maybe even full exported results), but for that, the challenge's creator has to always complete it, so that's not great for automation (otherwise it's unauthorized).
