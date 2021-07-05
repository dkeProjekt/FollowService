# FollowService

### SET-UP

#### 1) Aufruf in der Konsole:

`docker run --publish=7474:7474 --publish=7687:7687 -e 'NEO4J_AUTH=neo4j/secret' neo4j:4.2.4`

#### 2) Docker Desktop öffnen und neo4j Datenbank im Browser öffnen -> Passwort auf "secret" ändern


### REST-CALLS

#### 1) User anlegen

`localhost:5005/create`

###### Request: 

`{
"name" : "Benjamin"
}`

#### 2) User folgen

`localhost:5005/follow`

###### Request:

`{
"name" : "Benjamin",
"followName": "Florian"
}`

#### 3) User nicht mehr folgen

`localhost:5005/unfollow`

###### Request:

`{
"name" : "Benjamin",
"unfollowName": "Florian"
}`

#### 4) User folgt diesen Personen

`localhost:5005/getfollowed`

###### Response:

`{
	"get_all_users_following_successful": "True",
	"list_of_users_following": ["Elton", "Anna", "Tony"]
}`
