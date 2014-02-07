#!/bin/bash

mahout recommenditembased --input input/mydata --usersFile input/user.dat --numRecommendations 2 --output mahout_output/ --similarityClassname SIMILARITY_PEARSON_CORRELATION
