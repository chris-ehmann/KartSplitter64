# KartSplitter64

KartSplitter64 is an **in-development** auto-splitter made for Mario Kart 64. It uses a combination of template matching and predictions via a CNN to analyze gameplay frame-by-frame.

## Features

**Automatic Starts and Resets:** KartSplitter64 can determine whether or not a reset has occurred, and automatically reset LiveSplit for you. Likewise, it can automatically start a run for you. Please note that the timer will be incremented by 3 seconds to account for the delay between when a run actually starts, and when the program can confidently detect that a run has started.

**Automatic Splits:** Each frame of gameplay is analyzed by being passed through a neural network to determine whether it is after a track has finished. Once the program has detected such a frame with a reasonably high probability (>.90), the program will then automatically split on LiveSplit.

## Usage

**Required Python Version:** `3.10.7`
(Older or newer versions may work, but I can't guarantee that.)

KartSplitter64 is in a very early stage of development, currently being a minimally viable product. As such, you'll need to run the program via command line. You will need to install the required dependencies first, which you can do by navigating to the root directory of this project, and running 
```
pip install -r requirements.txt
```

You can then simply run the file `mk64as.py` located inside the `kartsplitter` directory. **Please make sure that LiveSplit Server is currently running before you do this! Also, check to make sure that the LiveSplit Server is configured to the default settings (i.e., "Server Port" is set to 16384). This will be changed in the future to be customizable.**

## Bug Reporting/Feature Requests
TBD. Some stuff is already planned (such as a user interface where you can select your capture window and easily define the gameplay region), but for any changes or issues, please use [![GitHub issues](https://img.shields.io/github/issues/chris-ehmann/KartSplitter64.svg?style=plastic)](https://github.com/chris-ehmann/KartSplitter64/issues)

Code quality is terrible at the moment. This is simply because I wanted to have a working program as fast as possible. Improvements will be made over time 🙂








