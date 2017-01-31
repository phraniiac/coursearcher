## Coursearcher
***
> Find MOOCS from a single place.

This is a simple implementation of BFS to create a Search Engine.
Find courses from
* Khan Academy
* Edx
* MIT OCW
* Udemy

### Tools Used
* Google App Engine
* Beautiful Soup 4
* Sitemaps of various sites.
* Python
* Jinja2
* Google Search API
* Google App Engine NDB Model.
* Twitter Bootstrap. ( *Soon to be changed to materializecss* )

### API (*Future tasks.*)
***
There are several features in the API. Below are the steps. The api is REST standards.
And the requests, and responses are handles in JSON.
#### Resources.
##### Query
A query object has following attributes.
* searchquery
* numres (*Number of Results required.*)
* source
##### Result
A result object has following attributes.
* link
* description
* source
##### Entry point of API.
* Entry Url
``/api``
