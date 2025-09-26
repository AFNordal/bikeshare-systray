# bikeshare-systray
Show the number of available bikes in your favorite bikeshare stations, directly in the windows systray! Your provider must use the [GBFS](https://github.com/MobilityData/gbfs/blob/master/gbfs.md) spec, like [Trondheim bysykkel](https://trondheimbysykkel.no/) and [Oslo bysykkel](https://oslobysykkel.no/) do:-D

![Demo](demo.png)

## Configuration
Update `config.py` with your provider URL, client ID and desired stations. To run the app manually, run `main.py`. Client ID is just a string that identifies you and your application.

### Run on startup
To make the app run on startup, simply run `install.bat` in the project directory. This will add a launch script to your startup directory and show it to you, and them start the app.

### Uninstall
To undo the installation, you only need to delete the launch file from your startup directory: Press `windows key` + `R` and run "shell:startup", then delete the file `bikeshare-systray-launcher.bat`.

## Usage
To reload the stations, right-click the icon and click "Refresh".
