# nct6795-fancontrol
Fan control GUI for NCT6795 Chip. This project is intended as a practicing project for interacting with sysfs and to learn python-GTK.

Chip used for this project is NCT6795 which is found in following motherboards (help to extend this list):
- MSI Gaming PRO MAX X470

This fancontrol app is possible to work also with other monitoring chips using the same [nct6775](https://github.com/torvalds/linux/blob/master/drivers/hwmon/nct6775.c) driver, though there is no possibility for me to test these.

## Usage
Program can be run in both normal user mode and root user mode. In normal user mode only monitoring and saving is allowed. To change fan speeds or modes, please run program as sudo.

Program can be run in command line mode as
```
chmod +x main.py # add execute permission for this file
./main.py
```

or using GTK3+ (though no functionality yet)
```
./main.py --gtk
```

## Dependencies
None