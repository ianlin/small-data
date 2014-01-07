#!/bin/bash

# sed for removing ^M
redirect_url=$(curl -i -s -X PUT "http://localhost:50070/webhdfs/v1/user/cloudera/band_charts.from_webhdfs?user.name=cloudera&op=CREATE" | grep Location | awk '{print $NF}' | sed 's/[[:cntrl:]]//')

curl -i -X PUT -T band_charts "$redirect_url"
