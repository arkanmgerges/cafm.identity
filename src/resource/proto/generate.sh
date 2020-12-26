#!/bin/bash

BLUE="\x1b[34;21m"
GREEN="\x1b[32;21m"
YELLOW="\x1b[33;21m"
RED="\x1b[31;21m"
RESET="\x1b[0m"

CURRENT_DIR_PATH=$(dirname "$0")
CURRENT_DIR_NAME=$(dirname "$0" | xargs basename)
echo -e "${GREEN}Generating proto code in path ${BLUE}'${CURRENT_DIR_PATH}'${RESET}"
echo -e "${GREEN}Current dir name is ${BLUE}'${CURRENT_DIR_NAME}'${RESET}"
echo -e "${GREEN}Current dir path is ${BLUE}'${CURRENT_DIR_PATH}'${RESET}"

TMPDIR="${CURRENT_DIR_PATH}"/tmpdir
mkdir -p "$TMPDIR"
SOURCE="${CURRENT_DIR_PATH}"
cp -r "$SOURCE"/*.proto "$TMPDIR"
echo -e ${YELLOW}
python -m grpc_tools.protoc --python_out=_generated --grpc_python_out=_generated -I "$TMPDIR" "$TMPDIR"/*.proto
echo -e ${RESET}
rm -rf "$TMPDIR"
