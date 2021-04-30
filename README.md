# Open-Source Firmware MultimediaCase for Raspberry Pi

## STM32

The following code defines the firmware for the STM32 controller of the RB-MultimediaCase01. The code uses the Infrared-Multiprotocoll-Decoder (IRMP - licensed under GNU General Public License v3.0) to recognize IR-remote signals and process these. The WS2812B LEDs can be controlled with the STM32 controller or with the Raspberry Pi. The Case Button
is handled by an interrupt routine.

The STM32 is mainly used to control the power status of the connected Raspberry Pi. It is able to power the Raspberry Pi via the 5 V pins and can send a shutdown-command via serial (which is processed via an addon). After shutdown of the Raspberry Pi the STM32 cuts the 5 V supply.

During the different routines (starting, shutdown, learning) the STM32 takes the control of the 4 WS2812B and displays the actual active routine with the help of colors.

Please refer to the additional comments in the corresponding sections for further explanations.


## Addons

These are the addons which we use for the functionality of the MultimediaCase.


## Config-Scripts/service.autoexec

The Config-Scripts/service.autoexec folder keeps the files of our setup routine. This routine is used for the intitial setup of an image.

## Firmware

Here you can find the compiled firmware binary file history.

## RaspberryPiOS Scripts

These scripts are edited for the use with Raspberry Pi OS.

## Source

This Folder contains the source and project files of the STM32 firmware.

## Download the addons

MultimediaCase: [Download](https://joy-it.net/public/script.module.MultimediaCase.zip)

HyperionMultimediaCase: [Download](https://joy-it.net/public/script.module.MCHyperion.zip)

RemoteControl: [Download](https://joy-it.net/public/script.remote.config.zip)


## Download the images

auto expanding LibreELEC image (2021-01-18): [Download](https://joyiteurope-my.sharepoint.com/:u:/g/personal/onedrive_joyiteurope_onmicrosoft_com/EQEVchu2KhNEsUVggU3ezTgBnFJMj6NfAHYnbeee-102Jg?e=phiWLe)

auto expanding LibreELEC 10.BETA image (2021-04-23): [Download](https://joyiteurope-my.sharepoint.com/:u:/g/personal/onedrive_joyiteurope_onmicrosoft_com/Eds0bwEG4Y9Hhxv23gmpEYIB8G4a9Mm-bEfDwDGMfCOWzA?e=qsyWuW)



If there are questions or something is unclear, please feel free
to contact us via E-Mail: service@joy-it.net
