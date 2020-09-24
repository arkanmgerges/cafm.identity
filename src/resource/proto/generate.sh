#!/bin/bash
CURRENT_DIR=`dirname "$0"`
FULL_PATH=$(echo "$(pwd)/${CURRENT_DIR}" | sed -E 's/\.\///g')
echo "Generating proto code in path ${FULL_PATH}"
python -m grpc_tools.protoc -I${FULL_PATH} --python_out="${FULL_PATH}/_generated" --grpc_python_out="${FULL_PATH}/_generated" "${FULL_PATH}"/pingpong.proto
