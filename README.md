# KartSplitter64

KartSplitter64 is an **in-development** auto-splitter made for Mario Kart 64. It uses a combination of template matching and predictions via a CNN to determine the current stage of the speedrun.

## Features

**Automatic Starts and Resets:** KartSplitter64 can determine whether or not a reset has occurred, and automatically reset LiveSplit for you. Likewise, it can automatically start a run for you. Please note that the timer will be incremented by 3 seconds to account for the delay between when a run actually starts, and when the program can confidently detect that a run has started.

**Automatic Splits:** Each frame of gameplay is analyzed by being passed through a neural network to determine whether it is after a track has finished. Once the program has detected such a frame with a reasonably high probability (>.90), the program will then automatically split on LiveSplit for you.

## Usage

**Python:** `3.10.7`

KartSplitter64 is in a very early stage of development, currently being a minimally viable product. As such, you'll need to run the program via command line.
