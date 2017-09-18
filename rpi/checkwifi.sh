#!/bin/bash

if ping -q -c 1 -W 1 10.0.1.1 >/dev/null; then
	exit 0
else
	exit 1
fi

