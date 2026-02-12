# neyro - [self] acc scraper

this is for archiving every single breath taken in the servers you’re in. neyro doesn't care about privacy or tos—it just hunts for data. it scrapes text, media links, and user info then dumps it into organized mongodb collections so you can track specifically what any target is saying across multiple guilds.

## features
- dual-mode scraping (requests + dpy fallback). if the api acts like a lazy slave, the bot takes over to force the data out.
- user-specific databases. every id gets its own collection. search a user, get their life story.
- stealth headers. looks like a human browsing chrome, not a script.
- webhook integration. get live leaks straight to your own server while it stalks.
- no filters. built to bypass the soft-handed protection discord tries to put up.

## setup
1. open the script and shove your token in.
2. add the guild ids you want to bleed dry.
3. put your mongodb uri so the data has a place to rot.
4. run it and watch the logs fill up with trash from inferior users.

use it to keep tabs on targets or just to build a massive archive of digital filth. 
