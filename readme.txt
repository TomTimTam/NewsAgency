Client API instructions:
Run the client using python3 client.py.

Example inputs for each user command.

login 'url'
	login http://ll14tac.pythonanywhere.com

logout
	logout
	
	logs out of the logged in service
	
post
	post
	
	followed by prompts for the news story's data. This will post to the
	logged in service.
	

news [agency_id] [category] [region] [yyyy/mm/dd]
	news [TAC] [pol] [eu] [2019/08/10]

	[agency_id] should be an id from the directory service.	
	[category] should be one of the following :pol, trivia, tech, art
	[region]   should be one of the following :eu, uk, w
	
	any empty brace will be treated as 'all'
	
	Caution : news [] [] [] [] will get every story from every service.

dlete 'story_key'
	delete 1
	
	will delete story with id 1 from from the logged in service.



