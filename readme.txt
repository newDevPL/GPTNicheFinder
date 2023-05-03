First clone the repo by making a new folder. Open command line or your terminal and navigate to your folder. Click on Code at the top of the page and the Download ZIP and extract it somewhere; or type in:
git clone https://github.com/newDevPL/GPTNicheFinder.git

Open the GPTNicheFinder folder and do the below:

1. Rename the file "rename_this_to_OpenAI.API" to OpenAI.API and replace its content with your OpenAI API key
2. In the app.py file replace the IP in the line 19 with the IP address of your computer and choose your preffered port (app.run(host='192.168.0.10', debug=True, port=8081))
3. Run the start.bat file
4. Open your browser using the link in the command prompt
5. Choose your GPT model, GPT 4 provides sloghtly better and more consistent results, while GPT 3.5 Turbo is cheaper to use and not everyone can access GPT 4 yet
6. Enter up to 5, comma separated, keywords or phrases. Keywords will give you broader results
7. Wait for the results, it might take up to few minutes


Known issues:

Entering more than 5 keywords or phrases will crash the application
Sometimes Google Trends returns "isPartial" which is interpreted as a niche by GPT and it starts hallucinating suggestions     
