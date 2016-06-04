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
var vcenterCfg = undefined;
var jobCfg = undefined;

JSONEditor.defaults.theme = 'bootstrap3';

function initAdmin() {

    jobsTable = $("#jobs-table").DataTable({
        "ordering": true,
        "order": [[1, "desc"]],
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
        createNewJob(jobdata[0], jobdata[3]);
    } );

    vcenterCfg = new JSONEditor(document.getElementById('vcenter-config'),{
                        schema: {
                          type: "object",
                          title: "vcenter",
                          properties: {
                            address: {
                              title: "Address",
                              type: "string",
                            },
                            port: {
                              title: "Port",
                              type: "integer",
                            },
                            username: {
                              title: "Username",
                              type: "string",
                            },
                            password: {
                              title: "Password",
                              type: "string",
                            },
                            monkey_template_name: {
                              title: "Monkey Template Name",
                              type: "string",
                            },
                            monkey_vm_info: {
                              title: "Monkey Creation VM",
                              type: "object",
                              properties: {
                                  name: {
                                      title: "Deployment Name",
                                      type: "string",
                                  },
                                  vm_folder: {
                                      title: "VM Folder (opt.)",
                                      type: "string",
                                  },
                                  resource_pool: {
                                      title: "Resource Pool (opt.)",
                                      type: "string",
                                  },
                                  datacenter_name: {
                                      title: "Datacenter (opt.)",
                                      type: "string",
                                  },
                                  cluster_name: {
                                      title: "Cluster (opt.)",
                                      type: "string",
                                  },
                                  datastore_name: {
                                      title: "Datastore (opt.)",
                                      type: "string",
                                  },
                              }
                            }
                          },
                          options: {
                            "collapsed": true
                          },                                           
                        },
                        disable_edit_json: false,
                        disable_properties: true,
                        });
    
    window.setTimeout(updateJobs, 5000);
    loadVcenterConfig();
    updateJobs();

}

function updateJobs() {
    $.getJSON('/job', function(json) {
        jobsTable.clear();
        var jobsList = json.objects;

        for (var i = 0; i < jobsList.length; i++) {
            jobsTable.row.add([jobsList[i].id, jobsList[i].creation_time, jobsList[i].type,jobsList[i].execution.state, JSON.stringify(jobsList[i].properties)]);
        }

        jobsTable.draw();
        //enableJobsSelect();
    });
}

function loadVcenterConfig() {
    $.getJSON('/connector?type=VCenterConnector', function(json) {
        vcenterCfg.setValue(json);
    });
}

function updateVcenterConfig() {
    var vc_config = vcenterCfg.getValue()
    vc_config["type"] = "VCenterConnector";

    $.ajax({
            headers : {
                'Accept' : 'application/json',
                'Content-Type' : 'application/json'
            },
            url : '/connector',
            type : 'POST',
            data : JSON.stringify(vc_config),
            success : function(response, textStatus, jqXhr) {
                console.log("New vcenter config successfully updated!");
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

function createNewJob(id, state) {
    if (!id) {
        jobsTable.$('tr.selected').removeClass('selected');
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
