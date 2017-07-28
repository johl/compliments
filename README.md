# Compliments

This is the server part of the Wikimedia Deutschland compliments
button. Together with a button connected to a NodeMCU/ESP8266 board,
it is meant to run on a Raspberry PI.

Showing appreciation for your colleagues is important! On the press
of a button, a random compliment is sent to a random colleague via
e-mail.

Of course you can still give compliments to colleagues directly in
the old-fashioned analogue way, but it's also important to keep up
with the cyber.

## Getting Started

Install the project from GitHub on you RaspberryPi. You need Python3.

### Prerequisites

Make sure you have the necessary libraries installed. Enter the `compliments` directory.

Run this:

```
pip3 install -r requirements.txt
```

## Running the service

Run it with `python3 compliments.py`.

## Hardware

You can find the necessary files for the compliments button client based on the NodeMCU ESP8266 at
[this GitHub repository](https://github.com/jakobw/compliments-button).

## Authors

* **Jens Ohlig <jens.ohlig@wikimedia.de>** - *Initial work* 
* **Lucas Werkmeister <lucas.werkmeister@wikimedia.de>** - *rewrite and most new features*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
