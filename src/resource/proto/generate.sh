#!/bin/bash
CURRENT_DIR_PATH=$(dirname "$0")
CURRENT_DIR_NAME=$(dirname "$0" | xargs basename)
echo "Generating proto code in path ${CURRENT_DIR_PATH}"
echo "Current dir name ${CURRENT_DIR_NAME}"
echo "Current dir path ${CURRENT_DIR_PATH}"

TMPDIR="${CURRENT_DIR_PATH}"/tmpdir
mkdir -p "$TMPDIR"
SOURCE="${CURRENT_DIR_PATH}"
cp -r "$SOURCE"/*.proto "$TMPDIR"

python -m grpc_tools.protoc --python_out=_generated --grpc_python_out=_generated -I "$TMPDIR" "$TMPDIR"/*.proto
rm -rf "$TMPDIR"
