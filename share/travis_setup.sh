#!/bin/bash
set -evx

mkdir ~/.dashcore

# safety check
if [ ! -f ~/.scrivcore/.scriv.conf ]; then
  cp share/scriv.conf.example ~/.scrivcore/scriv.conf
fi
