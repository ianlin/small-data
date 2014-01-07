#!/bin/bash

redirect_url=$(curl -i -s -X PUT "http://localhost:50070/webhdfs/v1/user/cloudera/band_charts.from_webhdfs?user.name=cloudera&op=CREATE" | grep Location | awk '{print $NF}')
curl -i -X PUT -T band_charts "$redirect_url"
