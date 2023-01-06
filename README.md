# QOTP

## Description

Welcome to the QOTP repository! QOTP is a desktop application designed to help you manage TOTP codes. The app is written in `Python` using `PySide6` and leverages the [pykeepass](https://github.com/libkeepass/pykeepass) library to provide a secure database for storing your TOTP codes.

## Current Features

- `Add entry`.  
   Add a new account to QOTP by either `loading a QR code image` or `pasting the QR code image` after taking a `screenshot` of the QR code. I recommend using [Flameshot](https://github.com/flameshot-org/flameshot) for taking screenshots on Windows and Linux.
- `Edit entry`.  
   Modify an entry display in QOTP, including the issuer name and username.
- `Export entry`.  
   Export an entry from QOTP as a QR code or secret key.
- `Delete entry`.  
   Remove an entry from QOTP.

## Installation

- Open a terminal window and navigate to the directory where you cloned the repository.
  ```bash
  cd /path/to/qotp
  ```
- Once in the `qotp` directory, navigate to the `src` directory.
  ```bash
  cd src
  ```
- Install the dependencies by running the following command.
  ```bash
  pip install -r requirements.txt
  ```
- Run the app.
  ```bash
  python3 main.py
  ```

## Usage

To begin managing your TOTP codes with QOTP, simply run the app and follow the prompts.
