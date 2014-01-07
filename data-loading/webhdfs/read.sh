#!/bin/bash

# sed for removing ^M
redirect_url=$(curl -i -s -X GET "http://localhost:50070/webhdfs/v1/user/cloudera/band_charts.from_webhdfs?user.name=cloudera&op=OPEN" | grep Location | awk '{print $NF}' | sed 's/[[:cntrl:]]//')

curl -X GET "$redirect_url"
