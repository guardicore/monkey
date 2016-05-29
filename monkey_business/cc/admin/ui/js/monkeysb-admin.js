/*const jsonFile = "/api/jbos";
var monkeys = null;
var generationDate = null;*/

// The JSON must be fully loaded before onload() happens for calling draw() on 'monkeys'
$.ajaxSetup({
    async: false
});

// Reading the JSON file containing the monkeys' informations
/*$.getJSON(jsonFile, function(json) {
    jobs = json.objects;
    generationDate = json.timestamp;
});*/

// Images/icons constants
const ICONS_DIR = "./css/img/objects/";
const ICONS_EXT = ".png";

// General options
// If variable from local storage != null, assign it, otherwise set it's default value.

var jobsTable = undefined;
var vcenterCfg = undefined;

JSONEditor.defaults.theme = 'bootstrap3';


function initAdmin() {

    jobsTable = $("#jobs-table").DataTable({
        "ordering": false,
    });

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
                                      type: "string",                                  },
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
                        startval: $,
                        });
    
    window.setTimeout(updateJobs, 10000);
    loadVcenterConfig();
    updateJobs();

}

function updateVCenterConf() {

}

function updateJobs() {
    $.getJSON('/job', function(json) {
        jobsTable.clear();
        var jobs = json.objects;

        for (var i = 0; i < jobs.length; i++) {
            jobsTable.row.add([jobs[i].timestamp, jobs[i].status, JSON.stringify(jobs[i].data)]);
        }

        jobsTable.draw();
    });

}

function loadVcenterConfig() {
    $.getJSON('/connector?type=vcenter', function(json) {
        vcenterCfg.setValue(json);
    });
}

function updateVcenterConfig() {
    var vc_config = vcenterCfg.getValue()
    vc_config["type"] = "vcenter";

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

function createNewJob() {
    elem = document.getElementById('job-config');
    elem.innerHTML = ""
    jobCfg = new JSONEditor(elem,{
                            schema: {
                              type: "object",
                              title: "Job",
                              properties: {
                                vlan: {
                                    title: "Vlan",
                                    type: "integer",
                                    $ref: "/info?type=vlans"
                                },
                              },
                              options: {
                                "collapsed": true
                              },
                            },
                            ajax: true,
                            disable_edit_json: false,
                            });
}

function configSched() {

}

/**
 * Manage the event when an object is selected
 */
function onSelect(properties) {

    /*if (properties.nodes.length > 0) {
        onNodeSelect(properties.nodes);
    }
    else
    {
        var content = "<b>No selection</b>"
        $("#selectionInfo").html(content);
        $('#monkey-config').hide()
        $('#btnConfigLoad, #btnConfigUpdate').hide();
        telemTable.clear();
        telemTable.draw();
    }*/

    /*if (properties.edges.length > 0) {
        onEdgeSelect(properties.edges);
    }*/

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
