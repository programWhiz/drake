#!/bin/bash -ex
cd "$(dirname "$0")"
echo "Building grammar..."
java -jar /usr/local/lib/antlr-4.7.1-complete.jar -Dlanguage=Python3 Drake.g4
echo "Done!"
