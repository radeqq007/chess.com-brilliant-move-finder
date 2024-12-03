# Chess.com brilliant move finder 

A python script to help find chess.com games with "brilliant" moves.

You need to have a chess.com [premium account](https://www.chess.com/membership?ref_id=74104030) to use this script
and have your insights generated.  

### Manual review is still required

Unfortunately, the chess.com API does not provide a way to directly
fetch games with brilliant moves. It does however provide the dates
of when the brilliant moves were played. This script is a workaround 
which fetches all the games played by a user on the given dates 
where a brilliant move was played. While it still requires you to 
manually check the games in the browser, it will drastically reduce
the amount of games you need to check and it's guaranteed to include
all the games with brilliant moves in the output csv. 
 


Usage:

```bash
pip install -r requirements.txt
python3 brilliant_move_finder.py <username>
```

This will genarate a csv file in the current directory with the 
format `<username>_potential_games.csv`

The csv file will contain the following columns:

```csv
brilliant,url,date,user_rating,opponent_rating,result,user_accuracy,opponent_accuracy
```

The `brilliant` column is left empty for you to quickly check the url of 
the game in the browser and mark it as brilliant or not. 