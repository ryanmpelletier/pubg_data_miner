# pubg_data_miner
Automatically download telemetry data files from your PUBG matches.

## Usage
1. `git clone https://github.com/ryanp102694/pubg_data_miner.git`
2. `cd pubg_data_miner/`
3. Replace YOUR_PUBG_USERNAME and YOUR_API_KEY in the script
4. Make sure python 3.7 is installed and that the "requests" package is installed
5. python pubg_data_miner.py (will take a while on the first run)

## End Result
The end result of running is several files in the project directory being downloaded. Each is named with a UUID for the telemetry. The matches.txt file is updated with IDs of matches you downloaded telemetry for. The script does not download telemetry for matches which it has listed in matches.txt.

Set this up as a cron job and have some fun!
