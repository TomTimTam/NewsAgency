Client API instructions:
Run the client using python3 client.py.

Author login is: Username - ll14tac, Password - 123testing123

note: This couldn't be tested with the directory service as the python anywhere hosting has expired for the directory.
	The expected data was guessed from the specification sheet. To re-enable the directory service head to the
	configurations page on pythonanywhere and press reload at the top.

Example inputs for each user command.

login 'url'	
	login http://ll14tac.pythonanywhere.com

	Caution: Do NOT end your URL with '/'

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

delete 'story_key'
	delete 1
	
	will delete story with id 1 from from the logged in service.



