// The JSON must be fully loaded before onload() happens for calling draw() on 'monkeys'
$.ajaxSetup({
    async: false
});

// Images/icons constants
const ICONS_DIR = "./css/img/objects/";
const ICONS_EXT = ".png";

// General options
// If variable from local storage != null, assign it, otherwise set it's default value.

var jobsTable = undefined;
var logsTable = undefined;
var jobCfg = undefined;
var conCfg = undefined;
var selectedJob = undefined;

JSONEditor.defaults.theme = 'bootstrap3';

function initAdmin() {

    jobsTable = $("#jobs-table").DataTable({
        "ordering": true,
        "order": [[1, "desc"]],
    });
    logsTable = $("#logs-table").DataTable({
        "ordering": false,
    });
    jobsTable.on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            jobsTable.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
        jobdata = jobsTable.row(this).data();
        selectedJob = jobdata[0];
        createNewJob(selectedJob, jobdata[3]);
        showLog(selectedJob);
    } );

    setInterval(updateJobs, 5000);
    setInterval(showLog, 5000);
    updateJobs();

}

function showLog() {
   logsTable.clear();

    if (!selectedJob) {
        return;
    }

    $.getJSON('/job?action=log&id=' + selectedJob, function(json) {
        var logsList = json.log;
        for (var i = 0; i < logsList.length; i++) {
            logsTable.row.add([logsList[i][0], logsList[i][1]]);
        }

        logsTable.draw();

    });
}

function updateJobs() {
    $.getJSON('/job', function(json) {
        jobsTable.clear();
        var jobsList = json.objects;

        for (var i = 0; i < jobsList.length; i++) {
            jobsTable.row.add([jobsList[i].id, jobsList[i].creation_time, jobsList[i].type,jobsList[i].execution.state, JSON.stringify(jobsList[i].properties)]);
        }

        jobsTable.draw();
    });
}

function loadConnectorsConfig() {
    elem = document.getElementById('connectors-config');
    elem.innerHTML = ""
    conCfg = new JSONEditor(elem,{
                                schema: {
                                  type: "object",
                                  title: "Connector",
                                  properties: {
                                        connector: {
                                            title: "Type",
                                            $ref: "/connector",
                                        }
                                  },
                                  options: {
                                    "collapsed": false
                                  },
                                },
                                ajax: true,
                                disable_edit_json: false,
                                disable_collapse: true,
                                disable_properties: true,
                                no_additional_properties: true
                                });
    conCfg.on('ready',function() {
        document.getElementById("btnSaveConnectorConfig").style.visibility = "visible";
    });
}

function updateConnectorConfig() {
    var con_config = conCfg.getValue()
    $.ajax({
            headers : {
                'Accept' : 'application/json',
                'Content-Type' : 'application/json'
            },
            url : '/connector',
            type : 'POST',
            data : JSON.stringify(con_config.connector),
            success : function(response, textStatus, jqXhr) {
                console.log("New vcenter config successfully updated!");
                document.getElementById("btnSaveConnectorConfig").style.visibility = "hidden";
                elem = document.getElementById('connectors-config');
                elem.innerHTML = ""
            },
            error : function(jqXHR, textStatus, errorThrown) {
                // log the error to the console
                console.log("The following error occured: " + textStatus, errorThrown);
            },
            complete : function() {
                console.log("Sending vcenter config update...");
            }
        });

}

function emptySelection() {
    showLog();
    selectedJob = undefined;
    jobsTable.$('tr.selected').removeClass('selected');
}

function createNewJob(id, state) {
    if (!id) {
        emptySelection();
    }

    elem = document.getElementById('job-config');
    elem.innerHTML = ""
    jobCfg = new JSONEditor(elem,{
                                schema: {
                                  type: "object",
                                  title: "Job",
                                  properties: {
                                        job: {
                                            title: "Type",
                                            $ref: "/jobcreate" + ((id)?"?id="+id:""),
                                        }
                                  },
                                  options: {
                                    "collapsed": false
                                  },
                                },
                                ajax: true,
                                disable_edit_json: false,
                                disable_collapse: true,
                                disable_properties: true,
                                no_additional_properties: true
                                });

    jobCfg.on('ready',function() {
        if (id && state != "pending") {
            jobCfg.disable();
            document.getElementById("btnSendJob").style.visibility = "hidden";
            document.getElementById("btnDeleteJob").style.visibility = "hidden";
        }
        else {
            jobCfg.enable();
            document.getElementById("btnSendJob").style.visibility = "visible";
            if (id) {
                document.getElementById("btnDeleteJob").style.visibility = "visible";
            }
            else {
                document.getElementById("btnDeleteJob").style.visibility = "hidden";
            }
        }
    });
}

function sendJob() {
    var job_config = jobCfg.getValue()

    $.ajax({
            headers : {
                'Accept' : 'application/json',
                'Content-Type' : 'application/json'
            },
            url : '/jobcreate',
            type : 'POST',
            data : JSON.stringify(job_config.job),
            success : function(response, textStatus, jqXhr) {
                console.log("Job successfully updated!");
                updateJobs();
            },
            error : function(jqXHR, textStatus, errorThrown) {
                // log the error to the console
                console.log("The following error occured: " + textStatus, errorThrown);
            },
            complete : function() {
                console.log("Sending job config...");
            }
        });
}

function deleteJob() {
    var job_config = jobCfg.getValue();
    if (job_config.job.id) {
            $.ajax({
            headers : {
                'Accept' : 'application/json',
                'Content-Type' : 'application/json'
            },
            url : '/jobcreate',
            type : 'GET',
            data : "action=delete&id=" + job_config.job.id,
            success : function(response, textStatus, jqXhr) {
                console.log("Job successfully updated!");
                updateJobs();
            },
            error : function(jqXHR, textStatus, errorThrown) {
                // log the error to the console
                console.log("The following error occured: " + textStatus, errorThrown);
            },
            complete : function() {
                console.log("Sending job config...");
            }
        });
    }
}

function configSched() {

}

/**
 * Clears the value in the local storage
 */
function clear(key) {
    if (localStorage[key]) {
        delete localStorage[key];
    }
};
/** /.localStorage Section **/
/** **/

/** ----- **/

/** **/
/** Utilities Section **/

/**
 * Returns the differences between two arrays
 */
Array.prototype.diff = function(other) {
    var diff = [];
    for (var i = 0; i < this.length; i++) {
        var obj = this[i];
        if (other.indexOf(obj) == -1) {
            diff.push(obj);
        }
    }
    for (var i = 0; i < other.length; i++) {
        var obj = other[i];
        if (this.indexOf(obj) == -1 && diff.indexOf(obj) == -1) {
            diff.push(obj);
        }
    }
    return diff;
};


/** /.Utilities Section **/
/** **/
