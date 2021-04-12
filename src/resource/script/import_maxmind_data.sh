#!/bin/sh

# @author: Arkan M. Gerges<arkan.m.gerges@gmail.com>

ensureIndexToCollection() {
  collectionName="$1"

  JS="
    const {db} = require('@arangodb');
    collection = db[\"$collectionName\"];
    collection.ensureIndex({type: 'persistent', fields: ['geoname_id']});
    collection.ensureIndex({type: 'persistent', fields: ['country_iso_code']});
  "
  arangosh \
    --server.endpoint tcp://arangodb:8529 \
    --server.database cafm-identity \
    --server.password ${CAFM_IDENTITY_ARANGODB_PASSWORD} \
    --javascript.execute-string "${JS}"
}

importFileToCollection() {
  collectionName=$1
  fileName=$2
  arangoimport --server.endpoint tcp://arangodb:8529 \
    --server.database cafm-identity --server.password ${CAFM_IDENTITY_ARANGODB_PASSWORD} \
    --create-collection true \
    --collection "${collectionName}" \
    --type csv \
    --file "${fileName}"
}

dropCollection() {
  collectionName=$1
  JS="
    const {db} = require('@arangodb');
    collection = db[\"$collectionName\"];
    collection.drop();
  "
  arangosh \
    --server.endpoint tcp://arangodb:8529 \
    --server.database cafm-identity \
    --server.password ${CAFM_IDENTITY_ARANGODB_PASSWORD} \
    --javascript.execute-string "${JS}"
}

collectionCount() {
  collectionName=$1
  JS="
  const {db} = require(\"@arangodb\");
  internal = require(\"internal\");
  try {
    internal.print(db._query(\"RETURN LENGTH($collectionName)\").next())
  }
  catch (error) {
    internal.print(\"0\")
  }"

  arangosh --server.endpoint tcp://arangodb:8529 \
    --server.database cafm-identity \
    --server.password ${CAFM_IDENTITY_ARANGODB_PASSWORD} \
    --javascript.execute-string "${JS}"
}

check_db() {
  JS="
  const {db} = require(\"@arangodb\");
  internal = require(\"internal\");
  try {
    internal.print(db._databases().includes(\"${CAFM_IDENTITY_ARANGODB_DB_NAME}\"))
  }
  catch (error) {
    internal.print(false)
  }"

  arangosh --server.endpoint tcp://arangodb:8529 \
    --server.database _system \
    --server.password ${CAFM_IDENTITY_ARANGODB_PASSWORD} \
    --javascript.execute-string "${JS}"
}

wait_for() {
  while :; do
    if [ "$(check_db)" = true ]; then
      break
    fi
    echo waiting for arangodb to be ready
    sleep 1
  done
}

# wait for arangodb to be ready
wait_for
# Import countries
if [ "$(collectionCount 'country')" -eq 0 ]; then
  importFileToCollection "country" "src/resource/maxmind/GeoLite2-Country-Locations-en.csv"
elif [ "$(collectionCount 'country')" -lt 252 ]; then
  dropCollection "country"
  importFileToCollection "country" "src/resource/maxmind/GeoLite2-Country-Locations-en.csv"
fi

# Import cities
if [ "$(collectionCount 'city')" -eq 0 ]; then
  importFileToCollection "city" "src/resource/maxmind/GeoLite2-City-Locations-en.csv"
elif [ "$(collectionCount 'city')" -lt 121259 ]; then
  dropCollection "city"
  importFileToCollection "city" "src/resource/maxmind/GeoLite2-City-Locations-en.csv"
fi

# Add indexes
ensureIndexToCollection 'country'
ensureIndexToCollection 'city'
