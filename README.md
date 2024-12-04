# Chess.com brilliant move finder 

A python script to help find chess.com games with "brilliant" moves.

You need to have a chess.com [premium account](https://www.chess.com/membership?ref_id=74104030) to use this script
and have your insights generated.  


### Donations 🥺

- [buymeacoffee](https://www.buymeacoffee.com/notjoemartinez)
- [paypal](https://paypal.me/notjoemartinez)
- [chess.com affiliate link](https://www.chess.com/membership?ref_id=74104030)

Usage:

```shell
git clone https://github.com/NotJoeMartinez/chess.com-brilliant-move-finder
cd chess.com-brilliant-move-finder
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 brilliant_move_finder.py <username> <time_class>
```

Where `<username>` is your chess.com username and `<time_class>` is either
rapid, blitz, bullet, daily. `<time_class>` is not required but is set 
to rapid by default. 

This will genarate a csv file in the current directory with the 
format `<username>_potential_<time_class>_games.csv`

The csv file will contain the following columns:

```csv
brilliant,url,date,openent_username,user_rating,opponent_rating,result,user_accuracy,opponent_accuracy
```

The `brilliant` column is left empty for you to quickly check the url of 
the game in the browser and mark it as brilliant or not. 


### Manual review (suggested)

Unfortunately, the chess.com API does not provide a way to directly
fetch games with brilliant moves. It does however provide the dates
of when the brilliant moves were played. This script is a workaround 
which fetches all the games played by a user on the given dates 
where a brilliant move was played. While it still requires you to 
manually check the games in the browser, it will drastically reduce
the amount of games you need to check and it's guaranteed to include
all the games with brilliant moves in the output csv. 


### Automated Review (use at your own risk)

The `browser_automation.py` script will automate the process of 
checking the csv outputed by `brilliant_move_finder.py` however 
it requires you have the FireFox browser installed and runs the 
risk of your account being banned for botting. If you don't want 
to risk that I recomend using a burner account. 

Usage: 

Create a new `.env` file like the one in `.env_example` with the 
path to your default firefox profile. You can find this directory
by going to `about:profiles` in the firefox url bar. 


**Make sure you are not running a firefox browser** at the same time you
run this script. Pass the csv file output by `brilliant_move_finder.py` 
as the first argument. 

```shell
python3 browser_automation.py username_potential_rapid_games.csv
```

This should spawn your firefox browser with all the bookmarks and 
cookies, it will try to begin itterating through the game analysis
of every game in the csv file. If you encounter a login screen,
login to your account and navigate back to your terminal and press 
enter, you should see 'Press Enter once you're logged in...' in the 
terminal. 

Suggestions: 

Try clicking around randomly as the browser goes through the games, 
this *might* reduce the chance of you encountering captchas.

Use this script on a throw away premiumn account, or try not to 
use this too much on an account you care about. chess.com is notorious
about banning bots. 