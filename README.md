# Spectrum

A database of shared resources

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

You *must* create a `.env` file to contain local environmental variables, the three that *must* be supplied are:

* SECRET_KEY
* DEBUG
* ALLOWED_HOSTS

### Installing

The project is managed using the [3 Musketeers](https://3musketeers.io/) methodology and uses GNU Make to run project tasks. Please see the Makefile for all of the rules.

To build the project

``` sh
make build
```

To start the web server

``` sh
make start
```

To tail the web server logs

``` sh
make logs
```

You can combine these together as normal in Make
``` sh
make build start logs
```

## Authors

* Neil Munro (NMunro) (nmunro@duck.com)

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

