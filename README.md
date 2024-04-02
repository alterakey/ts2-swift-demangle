# README

![Last release](https://img.shields.io/github/v/release/alterakey/ts2-swift-demangle)
![Last release date](https://img.shields.io/github/release-date-pre/alterakey/ts2-swift-demangle)
![Main branch deploy status](https://github.com/alterakey/ts2-swift-demangle/workflows/deploy/badge.svg)
![Main branch last commit](https://img.shields.io/github/last-commit/alterakey/ts2-swift-demangle/main)

ts2-swift-demangle is the Swift name demangling daemon for trueseeing, for environments that Swift installations are not available (e.g. containers).

It provides a RESTful API to resolve names.

## Usage

You need to boot it first, as follows:

    $ docker run -d --rm --name ts2-swift-demangle ghcr.io/alterakey/ts2-swift-demangle

Then you attach the trueseeing container to it like this, bringing up as http://ts2-swift-demangle (where trueseeing expects at):

    $ docker run ... --link ts2-swift-demangle trueseeing target.ipa
