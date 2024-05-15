# GTARadioPi
Pi / Python version of the GTA Radio. UI done with PyGame, may be switched to [Kivy](https://kivy.org/) in the future.

NOTE: some of the original diffs are on master branch isntead of main cause vscode

NOTE: Stations 8 & 11 in GTA IV were for user-made stations

## Usage
`python main.py -d "absolute/path/to/audio"`

## Design
A single state object is passed around, which functions will either read from (i.e. to get the curent audio to play), or will change the state (i.e. going to next track) before returning the updated state.

The state object is structured as follows:
```
{
    //Currently selected station
    "current": int
    "roor": str     //Root path
    "stations":[    //List of stations
        "type": int //Type of station, 0,1,2 (unsplit, split, talkshow)
        "name": str //Name of the station
        "src": str  //Absolute path to the station audio files
        "state": dict   //See below
    ]
}
```

For unsplit stations, 

For split and talkshow stations, which share a fairly similar structure and state management:
```
{
    "intermission":     bool    //If is currently in an intermission
    "news":             bool    //If intermission type is news
    "intermission_cnt": int     //How many intermissions there are left to play before returning to normal programming
    "track_id":         int     //Currently playing track id, used to track between track introductions and target track
    "introducing_track":bool    //If currently introducing next track (only type 1)          
}
```
