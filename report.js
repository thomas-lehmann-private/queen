angular.module('report', ['ui.bootstrap', 'gridshore.c3js.chart']);

/**
 * @ngdoc controller
 * @name report.controller:ReportController
 * @description
 * Provides all logic for querying performance details about the queen algorithm
 * implemented in different languages.
 */
angular.module('report').controller("ReportController", ['$scope', function($scope) {
    $scope.data = [];
    // loading JSON data
	var url = '/results/results.json';
    $.getJSON(url, function(data) {
        $scope.$apply(function() {
            $scope.data = data;
        });
    });

    /**
     * @ngdoc method
     * @name countDurations
     * @methodOf report.controller:ReportController
     * @description
     * Does count the measurements for one entry.
     * @param {object} durations dictionary with timestamps as key and duration as value.
     * @returns {int} count of measurements.
     */
    $scope.countDurations = function(durations) {
        var count = 0;
        for (key in durations) {
            count += 1;
        }
        return count;
    };

    /**
     * @ngdoc method
     * @name averageDuration
     * @methodOf report.controller:ReportController
     * @description
     * Does calculate the average duration for one entry.
     * @param {object} durations dictionary with timestamps as key and duration as value.
     * @returns {float} average duration.
     */
    $scope.averageDuration = function(durations) {
        var total = 0;
        var count = 0;
        for (key in durations) {
            total += durations[key];
            count += 1;
        }
        return total / count;
    }

    /**
     * @ngdoc method
     * @name customSort
     * @methodOf report.controller:ReportController
     * @description
     * Descending sort by chessboard with and then ascending by
     * best average duration. The best performance language you
     * should see at the top of the table.
     */
    $scope.customSort = function(entryA, entryB) {
        var diff = entryB.value["chessboard-width"] - entryA.value["chessboard-width"];
        if (diff == 0) {
            diff = $scope.averageDuration(entryA.value["durations"]) -
                $scope.averageDuration(entryB.value["durations"]);
        }
        return diff;
    };

    /**
     * @ngdoc method
     * @name numberOfLanguages
     * @methodOf report.controller:ReportController
     * @description
     * Number of languages.
     * @returns {int} nummber of languages.
     */
    $scope.numberOfLanguages = function() {
        var languages = {};
        for (var ix = 0; ix < $scope.data.length; ++ix) {
            languages[$scope.data[ix].language] = 0;
        }
        return Object.keys(languages).length;
    }

    /**
     * @ngdoc method
     * @name getDurationData
     * @methodOf report.controller:ReportController
     * @description
     * Number of languages.
     * @param {object} entry dictionary representing one language, version and chessboard size.
     * @returns {array} array with pairs of timestamp and duration.
     */
    $scope.getDurationData = function(entry) {
        var sorted = []
        for (var key in entry.durations) {
            sorted.push([key, entry.durations[key]]);
        }

        sorted.sort(function(a, b) {
            return a[0] - b[0];
        });

        return sorted;
    }

    /**
     * @ngdoc method
     * @name join
     * @methodOf report.controller:ReportController
     * @description
     * does provide a comma separated list of values.
     * @param {array} data array with each entry again an array of values.
     * @param {int} index the index of the value of one entry to take.
     * @returns {string} string with comma separated values. 
     */
    $scope.join = function(data, index) {
        var values = ""
        for (var x = 0; x < data.length; ++x) {
            if (x > 0) {
                values += ","
            }
            values += data[x][index];
        }

        return values;
    }

    /**
     * @ngdoc method
     * @name getDurationDataPerChessboardSize
     * @methodOf report.controller:ReportController
     * @description
     * array with each entry being a pair of two values: chessboard size
     * and the average duration. The result will be an ascending sort
     * by chessboard width.
     * @param {object} entry dictionary representing one language, version and chessboard size.
     * @returns {array} array with pairs of chessboard width and average duration.
     */
    $scope.getDurationDataPerChessboardSize = function(entry) {
        var sorted = []
        for (i in $scope.data) {
            if ($scope.data[i].language === entry.language &&
                $scope.data[i].version === entry.version &&
                $scope.data[i].source === entry.source &&
                $scope.data[i]["chessboard-width"] >= 12) {
                sorted.push([
                    $scope.data[i]["chessboard-width"],
                    $scope.averageDuration($scope.data[i].durations)
                ]);
            }
        }

        sorted.sort(function(a, b) {
            return a[0] - b[0];
        });

        return sorted;
    }
}]);