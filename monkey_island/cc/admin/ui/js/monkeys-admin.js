const jsonFile = "/api/monkey";
const jsonFileTelemetry = "/api/telemetry";
var monkeys = null;
var scannedMachines = [];
var generationDate = null;
var temelGenerationDate = null;

// The JSON must be fully loaded before onload() happens for calling draw() on 'monkeys'
$.ajaxSetup({
    async: false
});

// Reading the JSON file containing the monkeys' informations
$.getJSON(jsonFile, function(json) {
    monkeys = json.objects;
    generationDate = json.timestamp;
});


// The objects used by vis
var network = null;
var nodes = [];
var edges = [];

// Images/icons constants
const ICONS_DIR = "./css/img/objects/";
const ICONS_EXT = ".png";

const EDGE_TYPE_PARENT = "parent";
const EDGE_TYPE_TUNNEL = "tunnel";
const EDGE_TYPE_SCAN = "scan";

// General options
// If variable from local storage != null, assign it, otherwise set it's default value.

var focusedOnNode = false; 

var monkeyCfg = undefined;
var newCfg = undefined;
var telemTable = undefined;
JSONEditor.defaults.theme = 'bootstrap3';


function initAdmin() {
    if (monkeys == null) {
        errorMessage = "<font color='red'>Could not find '" + jsonFile + "'.</font>";
        $("#networkmap").html(errorMessage);
    }

    nodes = [];
    edges = [];

    createEdges();
    createTunnels();
    createScanned();

    var data = {
        nodes: createNodes(),
        edges: edges
    };

    var options = {
    };

    // Using jQuery to get the element does not work with vis.js library
    var container = document.getElementById("monkeysmap");

    network = new vis.Network(container, data, options);

    prepareSearchEngine();

    monkeyCfg = new JSONEditor(document.getElementById('monkey-config'),{
                            schema: {
                              type: "object",
                              title: "Monkey",
                              properties: {
                                alive: {
                                  title: "Alive",
                                  type: "boolean",
                                },                              
                              },
                              options: {
                                "collapsed": true
                              },                                           
                            },
                            disable_edit_json: false,
                            });

    newCfg = new JSONEditor(document.getElementById('new-config'),{
                            schema: {
                              type: "object",
                              title: "New Monkeys",
                              properties: {
                                alive: {
                                  title: "Alive",
                                  type: "boolean",
                                },                                                     
                              },
                              options: {
                                "collapsed": true
                              },                                  
                            },
                            disable_edit_json: false,
                            });
    newCfg.setValue({alive: true});

    telemTable = $("#telemetris-table").DataTable({
        "ordering": false,
    });

    window.setTimeout(updateMonkeys, 10000);

    addEventsListeners();
}

function updateMonkeys() {
    $.getJSON(jsonFile + '?timestamp='+ generationDate, function(json) {
        generationDate = json.timestamp;
        var new_monkeys = json.objects;
        for (var i = 0; i < new_monkeys.length; i++) {
            index = getMonkeyIndex(new_monkeys[i].guid);
            if(index != -1) {
                monkeys[index] = new_monkeys[i];
            }
            else
            {
                monkeys.push(new_monkeys[i]);
                nodes.push(createMonkeyNode(new_monkeys[i]));
            }
        }

        if(new_monkeys.length > 0)
        {
            createEdges();
            createTunnels();

            network.setData({nodes: nodes, edges: edges});
        }
        createScanned();
        window.setTimeout(updateMonkeys, 10000);
    });    
}

/**
 * Create the nodes used by vis.js
 */
function createNodes() {
    for (var i = 0; i < monkeys.length; i++) {
        var monkey = monkeys[i];

        nodes.push(createMonkeyNode(monkey));
    }
    return nodes;
}


function createMonkeyNode(monkey) {
    var title = undefined;
    var img = "monkey";

    if (monkey.description) {
        if(monkey.description.indexOf("Linux") != -1) {
            img = img + "-linux"
        }
        else if(monkey.description.indexOf("Windows") != -1) {
            img = img + "-windows"
        }
    }

    img = ICONS_DIR + img + ICONS_EXT;

    return {
            'id': monkey.id,
            'label': monkey.hostname + "\n" + monkey.ip_addresses[0],
            'shape': 'image',
            'color': undefined,
            'image': img,
            'title': title,
            'value': undefined,
            'mass': 0,
        };
}

function createMachineNode(machine) {
    img = ICONS_DIR + "computer" + ICONS_EXT;

    return {
            'id': machine.ip_addr,
            'label': machine.os.version + "\n" + machine.ip_addr,
            'shape': 'image',
            'color': undefined,
            'image': img,
            'title': undefined,
            'value': undefined,
            'mass': 0,
        };
}

function createEdges() {
    for (var i = 0; i < monkeys.length; i++) {
        var monkey = monkeys[i];
        if(monkey.parent != monkey.guid) {
            var parent = getMonkeyByGuid(monkey.parent);

            if(parent && !edgeExists([parent.id, monkey.id, EDGE_TYPE_PARENT])) {
                edges.push({from: parent.id, to: monkey.id, arrows:'middle', type: EDGE_TYPE_PARENT, color: 'red'});
            }
        }
    }

    return edges;
}

function createTunnels() {
    for (var i = 0; i < monkeys.length; i++) {
        var monkey = monkeys[i];
        if(monkey.tunnel_guid) {
            var tunnel = getMonkeyByGuid(monkey.tunnel_guid);

            if(tunnel && !edgeExists([monkey.id, tunnel.id, EDGE_TYPE_TUNNEL])) {
                edges.push({from: monkey.id, to: tunnel.id, arrows:'middle', type: EDGE_TYPE_TUNNEL, color:'blue'});
            }
        }
    }

    return edges;
}

function createScanned() {
    //For each existing monkey, gets all the scans performed by it
    //For each non exploited machine, adds a new node and connects it as a scanned node.
    for (var i = 0; i < monkeys.length; i++) {
        var monkey = monkeys[i];
        //Get scans for each monkey
        // Reading the JSON file containing the monkeys' informations
        $.getJSON(jsonFileTelemetry +'?timestamp='+ temelGenerationDate+ "&monkey_guid=" + monkey.guid+"&telem_type=scan", function(json) {
            temelGenerationDate = json.timestamp;
            var scans = json.objects;
            for (var i = 0; i < scans.length; i++) {
                var scan = scans[i];
                //Check if we already exploited this machine from another PoV, if so no point in scanning.
                if (null != getMonkeyByIP(scan.data.machine.ip_addr)) {
                    //if so, make sure we don't already have such a node
                    nodes = nodes.filter(function (node) {
                        return (node.id != ip_addr);
                    });
                    continue;
                }
                //And check if we've already added this scanned machine
                var machineNode = getScannedByIP(scan.data.machine.ip_addr)
                if (null == machineNode) {
                    machineNode = createMachineNode(scan.data.machine);
                    scannedMachines.push(machineNode);
                    nodes.push(machineNode);
                }

                if(!edgeExists([monkey.id, machineNode.id, EDGE_TYPE_SCAN])) {
                    edges.push({from: monkey.id, to: machineNode.id, arrows:'middle', type: EDGE_TYPE_SCAN, color: 'red'});
                }
            }
        });
    }
}

/**
 * Builds node description
 */
function buildMonkeyDescription(monkey) {
    var html =
        "<label>Name:</label> " + monkey.hostname + "</br>" +
        "<label>Description:</label> " + monkey.description + "</br>" +
        "<label>Internet Access:</label> " + monkey.internet_access + "</br>" +
        "<label>IP Address:</label></br>"

    for (var i = 0; i < monkey.ip_addresses.length; i++) {
        html += monkey.ip_addresses[i] + "</br>"
    }

    return html;
}


/**
 * Preparing the autocompletion search engine for the monkeys
 * TODO Upgrade the search with regex
 */
function prepareSearchEngine() {
    var engine = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace("hostname"),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local: this.monkeys
    });

    engine.initialize();

    $("#monkeySearch").typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        displayKey: "hostname",
        source: engine.ttAdapter()
    });

    $("#monkeySearch").keypress(function(event) {
        const ENTER_KEY_CODE = 13;
        if (event.which == ENTER_KEY_CODE) {
            selectNode(undefined, zoom=true);
        }
    });
}


/**
 * Manage the key presses events
 */
function onKeyPress(event){
    var charCode = ("charCode" in event) ? event.charCode : event.keyCode;
    console.log("Unicode '" + charCode + "' was pressed.");
}

/**
 * Adding the events listeners
 */
function addEventsListeners() {
    network.on("doubleClick", onDoubleClick);
    network.on("select", onSelect);
}

/**
 * Manage the event when an object is double-clicked
 */
function onDoubleClick(properties) {
    for (var i = 0; i < properties.nodes.length; i++) {
        network.focus(properties.nodes[i], {scale:1});
    }
    onSelect(properties);
}


/**
 * Manage the event when an object is selected
 */
function onSelect(properties) {

    if (properties.nodes.length > 0) {
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
    }

    if (properties.edges.length > 0) {
        onEdgeSelect(properties.edges);
    }

}

/**
 * Manage the event when a node is selected
 */
function onNodeSelect(nodeId) {
    var monkey = getMonkey(nodeId);

    var htmlContent = "";


    if (monkey) {
        htmlContent = buildMonkeyDescription(monkey);
        $("#monkeySearch").val(monkey.hostname);
    }

    $("#selectionInfo").html(htmlContent);

    $('#monkey-config').show()
    $('#btnConfigLoad, #btnConfigUpdate').show();


    $.getJSON('/api/telemetry/' + monkey.guid, function(json) {
        telemTable.clear();
        var telemetries = json.objects;

        for (var i = 0; i < telemetries.length; i++) {
            telemTable.row.add([telemetries[i].timestamp, telemetries[i].telem_type, JSON.stringify(telemetries[i].data)]);
        } 

        telemTable.draw();
    });


    network.selectNodes([nodeId]);
}

/**
 * Manage the event when an edge is selected
 */
function onEdgeSelect(edge) {
    var edge = getEdge(edge);

}


function toggleFocusOnNode() {
    if (focusedOnNode) {
        network.zoomExtent({duration:0});
        focusedOnNode = false;
    }
    else {
        selectNode(undefined, zoom=true);
    }
}

function loadNewMonkeysConfig() {
    $.getJSON('/api/config/new', function(json) {
        if (jQuery.isEmptyObject(json))
        {
            newCfg.setValue({alive: true});
        }
        else
        {
            if(undefined == json.alive)
            {
                json.alive = true;
            }
            delete json.id;
            newCfg.setValue(json);
        }
    });
}

function updateNewMonkeysConfig() {
    var curr_config = newCfg.getValue()

    $.ajax({
            headers : {
                'Accept' : 'application/json',
                'Content-Type' : 'application/json'
            },
            url : '/api/config/new',
            type : 'POST',
            data : JSON.stringify(curr_config),
            success : function(response, textStatus, jqXhr) {
                console.log("New monkeys config successfully updated!");
            },
            error : function(jqXHR, textStatus, errorThrown) {
                // log the error to the console
                console.log("The following error occured: " + textStatus, errorThrown);
            },
            complete : function() {
                console.log("Sending new monkeys config update...");
            }
        });
}

function loadMonkeyConfig() {
    nodes = network.getSelectedNodes();

    if(nodes.length != 1) {
        return;
    }

    var monkey = getMonkey(nodes[0]);

    monkeyCfg.setValue(monkey.config);
}

function updateMonkeyConfig() {
    nodes = network.getSelectedNodes();
    if(nodes.length != 1) {
        return;
    }

    var monkey = getMonkey(nodes[0]);

    var curr_config = monkeyCfg.getValue()

    $.ajax({
            headers : {
                'Accept' : 'application/json',
                'Content-Type' : 'application/json'
            },
            url : '/api/monkey/' + monkey.guid,
            type : 'PATCH',
            data : JSON.stringify({config: curr_config}),
            success : function(response, textStatus, jqXhr) {
                monkey.config = curr_config;
                console.log("Monkey config successfully updated!");
            },
            error : function(jqXHR, textStatus, errorThrown) {
                // log the error to the console
                console.log("The following error occured: " + textStatus, errorThrown);
            },
            complete : function() {
                console.log("Sending monkey config update...");
            }
        });
}


function selectNode(hostname, zoom) {
    if (hostname == undefined) {
        hostname = $("#monkeySearch").val();
    }

    if (hostname == "") {
        return;
    }

    for (var i = 0; i < monkeys.length; i++) {
        var monkey = monkeys[i];
        if (monkey.hostname == hostname) {
            onNodeSelect([monkey.id]);
            if (zoom) {
                network.focus(monkey.id, {scale:1});
                focusedOnNode = true;
            }
            break;
        }
    }
}


/**
 * Get a monkey from its id
 */
function getMonkey(id) {
    for (var i = 0; i < monkeys.length; i++) {
        if (monkeys[i].id == id) {
            return monkeys[i];
        }
    }
}

function getMonkeyByGuid(guid) {
    for (var i = 0; i < monkeys.length; i++) {
        if (monkeys[i].guid == guid) {
            return monkeys[i];
        }
    }    
}

function getMonkeyByIP(ip) {
        for (var i = 0; i < monkeys.length; i++) {
            var monkey = monkeys[i];
            for (var j = 0; j< monkey.ip_addresses; j++) {
                if (monkeys[i].ip == ip) {
                    return monkeys[i];
                }
            }
    }
    return null;
}

function getScannedByIP(ip)
{
        for (var i = 0; i < scannedMachines.length; i++) {
            var machine = scannedMachines[i];
            if (machine.id == ip) {
                return machine
            }
    }
    return null;
}

function getMonkeyIndex(guid) {
    for (var i = 0; i < monkeys.length; i++) {
        if (monkeys[i].guid == guid) {
            return i;
        }
    }
    return -1;
}

/**
 * Get a node from its id
 */
function getNode(id) {
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].id == id) {
            return nodes[i];
        }
    }
}

/**
 * Get an edge from its id
 */
function getEdge(id) {
    for (var i = 0; i < edges.length; i++) {
        if (edges[i].id == id) {
            return edges[i];
        }
    }
}

/**
 * Verifies whether a node already exist or not
 */
function nodeExists(id) {
    return getNode(id) != null;
}

/**
 * Verifies whether a link already exist or not
 */
function edgeExists(link) {
    for (var i = 0; i < edges.length; i++) {
        var from = edges[i].from;
        var to = edges[i].to;
        var type = edges[i].type;
        if (from == link[0] && to == link[1] && type == link[2]) {
            return true;
        }
    }
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
