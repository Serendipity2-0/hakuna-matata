1. ContentCalendar
2. Client Management System
3. CodingCalendar
4. AccountTaskCalendar
5. Employee Management System


1. ContentCalendar DB: 
  - Twitter
  - Facebook
  - Instagram
  - LinkedIn
  - YouTube
  - VC Pitch Deck
  - Blog
  - Email
  - Podcast
  - GeneralScripts

2. Client Management System DB:
  - Client Name
  - Client Email
  - Client Phone
  - Client Address
  - Client City
  - Client State
  - Client Zip
- CMSCalendar DB:
  - Date
  - Event
  - Description
  - Status
  - Due Date
  - Completed Date
  - Completed By
  - Project Name

1. CodingCalendar DB:
  - Coding Task
  - Coding Task Description
  - Coding Task Status
  - Coding Task Due Date
  - Coding Task Completed Date
  - Coding Task Completed By
  - Coding Project Name

2. AccountTaskCalendar DB:
  - Account Task
  - Account Task Description
  - Account Task Status
  - Account Task Due Date
  - Account Task Completed Date
  - Account Task Completed By
  - Account Task Project Name

3. Employee Management System DB:
  - Employee Name
  - Employee Email
  - Employee Phone
  - Employee Address
  - Employee City
  - Employee State
  - Employee Zip
  - Employee Date of Birth
  - Employee Start Date
  - Employee End Date
  - Employee Status
  - Employee Role
  - Employee Department
  - Employee Salary

4. Document Calendar DB:
  - Document Name
  - Document Description
  - Document Status
  - Document Due Date
  - Document Completed Date
  - Document Completed By

Help me build an interactive discord bot which can take the @DB/Main/Calendar.db file. Use prefix commands, slash commands, modals and other appropriate interactive tools like dropdowns, buttons, etc., to make it user friendly. 
Read the database before building the bot. 

Required functionalites:
1. Add a new event to the calendar
2. View all events in the calendar
3. Query the calendar for a specific date. Give choices of today, this week, custom date.
4. Delete an event from the calendar
5. Update an event in the calendar


Discord cogs for audio transcript:
command which takes audio file as an input and uses audio transcript to return back an MD file, save it, also displayed back in discord DISCORD_AUDI0MEET_CHANNEL_ID. give choice of backend/agents/tools/assemblyAudioTranscript.py and backend/agents/tools/geminiAudiotranscript.py . Save the MD file in DB/AudioTranscripts and audio in Assets/AudioMeet. Display response back in DISCORD_AUDI0MEET_CHANNEL_ID.

###############
Help me build an interactive discord bot in DISCORD_CMS_CHANNEL_ID which can take the @DB/Main/customer_management.db file. Use prefix commands, slash commands, modals and other appropriate interactive tools like dropdowns, buttons, etc., to make it user friendly. Place it in cogs/customer_management_commands.py

IMPORTANT: Read the database with sqlite3 commands before building the bot.


Required functionalites:
1. Add a new customer to the database
2. View all customers in the database based on Past, Active, Prospective
3. Schedule a call/meeting with a customer
4. Update meeting details
5. Meeting reminder
6. After meeting actions



