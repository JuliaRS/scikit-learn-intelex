#*******************************************************************************
# Copyright 2014-2018 Intel Corporation
# All Rights Reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License"), the following terms apply:
#
# You may not use this file except in compliance with the License.  You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#*******************************************************************************

# daal4py K-Means example for shared memory systems

import daal4py as d4p
from numpy import loadtxt, allclose

if __name__ == "__main__":

    infile = "./data/batch/kmeans_dense.csv"
    method = 'svdDense'
    nClusters = 10
    maxIter = 25

    # configure a kmeans-init
    initalgo = d4p.kmeans_init(nClusters, method="plusPlusDense")
    # Load the data
    data = loadtxt(infile, delimiter=',')
    # compute initial centroids
    initresult = initalgo.compute(data)
    # The results provides the initial centroids
    assert initresult.centroids.shape[0] == nClusters

    # configure kmeans main object: we also request the cluster assignments
    algo = d4p.kmeans(nClusters, maxIter, assignFlag=True)
    # compute the clusters/centroids
    result = algo.compute(data, initresult.centroids)
    
    # Note: we could have done this in just one line:
    # d4p.kmeans(nClusters, maxIter, assignFlag=True).compute(data, d4p.kmeans_init(nClusters, method="plusPlusDense").compute(data).centroids)

    # Kmeans result objects provide assignments (if requested), centroids, goalFunction, nIterations and objectiveFunction
    assert result.centroids.shape[0] == nClusters
    assert result.assignments.shape == (data.shape[0], 1)
    assert result.nIterations <= maxIter

    print('All looks good!')
