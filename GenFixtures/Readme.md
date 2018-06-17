
The script generates fixture that can be loaded by django.

Only Songs, Albums, BelongTos, Artists, and Releases are generated. You may want to manually add Users/PlayLists by django admin.

# Steps
### Make sure your DB is in a clean state
Otherwise django may complain about repeated object/relations.
### Make sure your working directory is GenFixtures/
### run get\_data.sh
this script will download music data from https://www.upf.edu/web/mtg/mard (~320MB)
### run gen\_fixtures.py
this script will try fetching lyrics of popular albums from lyricwikia, then output the result to `output.json`
(You can change the sellRank threshold in the script to generate more data)
### import output.json to db
run `./manage.py loaddata GenFixtures/output.json`

