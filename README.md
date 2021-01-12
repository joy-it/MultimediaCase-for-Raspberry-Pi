# Open-Source Firmware MultimediaCase for Raspberry Pi

## STM32

The following code defines the firmware for the STM32 controller of the RB-MultimediaCase01. The code uses the Infrared-Multiprotocoll-Decoder (IRMP - licensed under GNU General Public License v3.0) to recognize IR-remote signals and process these. The WS2812B LEDs can be controlled with the STM32 controller or with the Raspberry Pi. The Case Button
is handled by an interrupt routine.

The STM32 is mainly used to control the power status of the connected Raspberry Pi. It is able to power the Raspberry Pi via the 5 V pins and can send a shutdown-command via serial (which is processed via an addon). After shutdown of the Raspberry Pi the STM32 cuts the 5 V supply.

During the different routines (starting, shutdown, learning) the STM32 takes the control of the 4 WS2812B and displays the actual active routine with the help of colors.

Please refer to the additional comments in the corresponding sections for further explanations.


## Addons

These are the addons which we use for the functionality of the MultimediaCase.


## Starting Program

The starting-program folder keeps the files of our setup routine. This routine is used for the intitial setup of an image.

## Download the images

64GB Image: [Download](https://joyiteurope-my.sharepoint.com/:u:/g/personal/onedrive_joyiteurope_onmicrosoft_com/EX_NeiiZkCtBg7PNMkzbpgwBIQwNJXln7WyuMJqDdQwtEA?e=zAvC8Q)
32GB Image: [Download](https://joyiteurope-my.sharepoint.com/:u:/g/personal/onedrive_joyiteurope_onmicrosoft_com/EWgB0fqF5J5OvBvpzs6oe_kB3oDqyoTp9xweV5ClyKyMvw?e=G4fSnk)
16GB Image: [Download](https://joyiteurope-my.sharepoint.com/:u:/g/personal/onedrive_joyiteurope_onmicrosoft_com/EeiXyl3F1wlLkIXmxS_ccZwBVpN9eTzLnmOxJ8Ehb97xzA?e=Y6skRa)


If there are questions or something is unclear, please feel free
to contact us via E-Mail: service@joy-it.net
