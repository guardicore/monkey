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
var numOfParentLinks = 0;
var numOfTunnelLinks = 0;
var numOfScanLinks = 0;

var showScannedHosts = true;

// Images/icons constants
const ICONS_DIR = "./css/img/objects/";
const ICONS_EXT = ".png";

const HOST_TYPE_MONKEY = "monkey";
const HOST_TYPE_SCAN = "scanned";

const EDGE_TYPE_PARENT = "parent";
const EDGE_TYPE_TUNNEL = "tunnel";
const EDGE_TYPE_SCAN = "scan";

const EDGE_COLOR_PARENT = "red";
const EDGE_COLOR_TUNNEL = "blue";
const EDGE_COLOR_SCAN = "gray";

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

    createNodes();
    createEdges();
    createTunnels();
    createScanned();

    var data = {
        nodes: nodes,
        edges: edges
    };

    updateCounters();

    var options = {
        layout: {
            improvedLayout: false
        }/*,
        physics: {
            enabled: true
        }*/
    };

    // Using jQuery to get the element does not work with vis.js library
    var container = document.getElementById("monkeysmap");

    network = new vis.Network(container, data, options);

    $("[name='chboxShowScanned']").bootstrapSwitch('onSwitchChange', toggleScannedHosts);
    $("[name='chboxMonkeyEnabled']").bootstrapSwitch('onSwitchChange', toggleMonkeyEnabled);

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

    loadNewMonkeysConfig(); 

    setInterval(updateMonkeys, 10000);

    addEventsListeners();
}

function toggleScannedHosts(event, state) {
    if (event.type != "switchChange") {
        return;
    }
    if (state) {
        showScannedHosts = true;
    }
    else {
        showScannedHosts = false;
    }
    refreshDrawing();
}

function refreshDrawing() {
    // function called before first init
    if (network == null) {
        return;
    }

    // keep old selection
    var selNode = network.getSelectedNodes();

    if (showScannedHosts) {
        network.setData({nodes: nodes, edges: edges});
    }
    else {
        var selectiveNodes = [];
        var selectiveEdges = [];
        for (var i=0; i<nodes.length; i++) {
            if (nodes[i].type != HOST_TYPE_SCAN) {
                selectiveNodes.push(nodes[i])
            }
        }
        for (var i=0; i<edges.length; i++) {
            if (edges[i].type != EDGE_TYPE_SCAN) {
                selectiveEdges.push(edges[i])
            }
        }
        network.setData({nodes: selectiveNodes, edges: selectiveEdges});
    }

    if (selNode.length) {
        var monkey = getMonkey(selNode[0]);
        if (monkey) { // The selection might be no longer valid if the monkey was deleted
            selectNode(monkey.hostname, false);
        }
    }
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
                var exiting_scan = undefined;
                for (var j=0; j<new_monkeys[i].ip_addresses.length; j++) {
                    exiting_scan = getScannedByIP(new_monkeys[i].ip_addresses[j]);
                    if (exiting_scan != undefined) {
                        break;
                    }
                }
                if (exiting_scan == undefined) {
                    nodes.push(createMonkeyNode(new_monkeys[i]));
                }
                else {
                    convertScanNodeToMonkey(exiting_scan, new_monkeys[i]);
                }
                updateCounters();
            }
        }

        if(new_monkeys.length > 0)
        {
            createEdges();
            createTunnels();
            refreshDrawing();
        }
        createScanned();
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
    var font = undefined;
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

    if (monkey.parent == null) {
        font = { color: 'red' };
    }
    else {
        for (var i=0; i<monkey.parent.length; i++) {
            if (monkey.parent[i][1] == null) {
                font = { color: 'red' };
            }
        }
    }

    return {
            'id': monkey.id,
            'label': monkey.hostname + "\n" + monkey.ip_addresses[0],
            'font': font,
            'shape': 'image',
            'color': undefined,
            'image': img,
            'title': title,
            'value': undefined,
            'type' : HOST_TYPE_MONKEY,
            'mass': 1,
        };
}

function createMachineNode(machine) {
    img = "computer";

    if (undefined != machine.os.type) {
        if (machine.os.type == "linux") {
            img += "-linux";
        }
        else if (machine.os.type == "windows") {
            img += "-windows";
        }
    }

    img = ICONS_DIR + img + ICONS_EXT;

    return {
            'id': machine.ip_addr,
            'label': machine.os.version + "\n" + machine.ip_addr,
            'shape': 'image',
            'color': undefined,
            'image': img,
            'title': undefined,
            'value': undefined,
            'type' : HOST_TYPE_SCAN,
            'mass': 1,
        };
}

function convertScanNodeToMonkey(scanned, monkey) {
    var monNode = createMonkeyNode(monkey);
    nodes.push(monNode);

    // move edges to new node
    for (var i = 0; i < edges.length; i++) {
        if (edges[i].to == scanned.id) {
            edges[i].to = monNode.id;
        }
        if (edges[i].from == scanned.id) {
            edges[i].from = monNode.id;
        }
    }
    for (var i=0; i<scannedMachines.length; i++) {
        if (scannedMachines[i].id == scanned.id) {
            scannedMachines.splice(i, 1);
            break;
        }
    }
    for (var i=0; i<nodes.length; i++) {
        if (nodes[i].id == scanned.id) {
            nodes.splice(i, 1);
            break;
        }
    }
}

function createEdges() {
    for (var i = 0; i < monkeys.length; i++) {
        var monkey = monkeys[i];

        if (monkey.parent == null) { continue; };

        for (var j=0; j<monkey.parent.length; j++) {
            if(monkey.parent[j][0] != monkey.guid) {
                var parent = getMonkeyByGuid(monkey.parent[j][0]);
                var exploit = monkey.parent[j][1];

                if(parent && !edgeExists([parent.id, monkey.id, EDGE_TYPE_PARENT])) {
                    var title = "<center><b>" + exploit + "</b></center>From: " + parent.hostname + "<br/>To: " + monkey.hostname;
                    edges.push({from: parent.id, to: monkey.id, arrows:'middle', type: EDGE_TYPE_PARENT, title: title, /*label: exploit, font: {color: 'red', size: 10, align: 'top'},*/ color: EDGE_COLOR_PARENT});
                    if (removeEdge([parent.id, monkey.id, EDGE_TYPE_SCAN])) {
                        numOfScanLinks--;
                    }
                    numOfParentLinks++;
                }
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
                edges.push({from: monkey.id, to: tunnel.id, arrows:'middle', type: EDGE_TYPE_TUNNEL, color: EDGE_COLOR_TUNNEL});
                numOfTunnelLinks++;
            }
        }
    }

    return edges;
}

function createScanned() {
    // Gets all the scans performed by monkeys
    // For each non exploited machine, adds a new node and connects it as a scanned node.

    // Reading the JSON file containing the monkeys' informations
    $.getJSON(jsonFileTelemetry +'?timestamp='+ temelGenerationDate + "&telem_type=scan", function(json) {
        temelGenerationDate = json.timestamp;
        var scans = json.objects;
        for (var i = 0; i < scans.length; i++) {
            var scan = scans[i];
            var monkey = getMonkeyByGuid(scan.monkey_guid);

            // And check if we've already added this scanned machine
            var machineNode = getMonkeyByIP(scan.data.machine.ip_addr);

            if (null == machineNode) {
                machineNode = getScannedByIP(scan.data.machine.ip_addr);

                if (null == machineNode) {
                    machineNode = createMachineNode(scan.data.machine);
                    scannedMachines.push(machineNode);
                    nodes.push(machineNode);
                }
            }

            if(!edgeExists([monkey.id, machineNode.id, EDGE_TYPE_SCAN]) && !edgeExists([monkey.id, machineNode.id, EDGE_TYPE_PARENT])) {
                edges.push({from: monkey.id, to: machineNode.id, arrows:'middle', type: EDGE_TYPE_SCAN, color: EDGE_COLOR_SCAN});
                numOfScanLinks++;
            }
        }
        if (scans.length > 0) {
            refreshDrawing();
            updateCounters();
        }
    });
}

/**
 * Builds node description
 */
function buildMonkeyDescription(monkey) {
    var html =
        "<label>Name:</label> " + monkey.hostname + "</br>" +
        "<label>Description:</label> " + monkey.description + "</br>" +
        "<label>Internet Access:</label> " + monkey.internet_access + "</br>";
    if (monkey.dead) {
        html += "<label>State:</label> Dead </br>";
    }
    if (!monkey.config.alive) {
        html += "<label>Note:</label> Marked to be dead</br>";
    }
    html +=
        "<label>Last Seen:</label> " + monkey.keepalive + "</br>" +
        "<label>IP Address:</label><br/>";

    html += "<ul>";
    for (var i = 0; i < monkey.ip_addresses.length; i++) {
        html += "<li>" + monkey.ip_addresses[i];
    }
    html += "</ul>";


    if (monkey.parent != null) {
        html += "<label>Exploited by:</label><br/>"
        html += "<ul>";
        for (var i = 0; i < monkey.parent.length; i++) {
            html += "<li>";
            if (monkey.parent[i][0] == monkey.guid) {
                html += "Manual Run<br/>";
            }
            else {
                parent = getMonkeyByGuid(monkey.parent[i][0]);
                if (!parent) { html += "Unknown Source"; continue; }

                html +=  parent.hostname + " (";
                if (monkey.parent[i][1] == null) {html += "Unknown"}
                else {html += monkey.parent[i][1];}
                html += ")";
            }
        }
        html += "</ul>";
    }

    return html;
}

function updateCounters() {
    $('#infoNumOfMonkeys').html(monkeys.length);
    $('#infoNumOfHosts').html(scannedMachines.length);
    $('#infoNumOfParents').html(numOfParentLinks);
    $('#infoNumOfTunnels').html(numOfTunnelLinks);
    var numOfAlive = monkeys.length;
    for (var i=0;i<monkeys.length;i++) {
        if (monkeys[i].dead) {numOfAlive--;}
    }
    $('#infoNumOfAlive').html(numOfAlive);
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

    if ((properties.nodes.length > 0) && getMonkey(properties.nodes[0])){
        onNodeSelect(properties.nodes);
    }
    else
    {
        var content = "<b>Monkey not selected</b>"
        $("#selectionInfo").html(content);
        $('#monkey-config').hide()
        $('#btnConfigLoad, #btnConfigUpdate').hide();
        $('#monkey-enabled').hide();
        telemTable.clear();
        telemTable.draw();

        if (properties.edges.length > 0) {
            onEdgeSelect(properties.edges);
        }
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
        $("#selectionInfo").html(htmlContent);
        $('#monkey-config').show()
        $('#btnConfigLoad, #btnConfigUpdate').show();

        loadMonkeyConfig();

        if (monkey.config.alive) {
            $("[name='chboxMonkeyEnabled']").bootstrapSwitch('state', true, true);
        }
        else {
            $("[name='chboxMonkeyEnabled']").bootstrapSwitch('state', false, true);
        }
        $('#monkey-enabled').show();

        $.getJSON('/api/telemetry?monkey_guid=' + monkey.guid, function(json) {
            telemTable.clear();
            var telemetries = json.objects;

            for (var i = 0; i < telemetries.length; i++) {
                telemTable.row.add([telemetries[i].timestamp, telemetries[i].telem_type, JSON.stringify(telemetries[i].data)]);
            }

            telemTable.draw();
        });
    }

    network.selectNodes([nodeId]);
}

/**
 * Manage the event when an edge is selected
 */
function onEdgeSelect(edge) {
    var edge = getEdge(edge);
    var monkey = getMonkey(edge.from);
    if (!monkey) {return;};

    var target = undefined;
    if (edge.type == 'scan') {
        target = getScannedByIP(edge.to)
    }
    else {
        target = getMonkey(edge.to)
    }

    $.getJSON(jsonFileTelemetry + '?monkey_guid=' + monkey.guid, function(json) {
        telemTable.clear();
        var telemetries = json.objects;

        for (var i = 0; i < telemetries.length; i++) {
            var telem = telemetries[i]
            if (telem.telem_type == 'scan' || telem.telem_type == 'exploit') {
                if (((edge.type == 'scan') && (telem.data.machine.ip_addr == target.id)) ||
                    ((edge.type == 'parent') && (0 <= $.inArray(telem.data.machine.ip_addr, target.ip_addresses)))) {
                    telemTable.row.add([telemetries[i].timestamp, telemetries[i].telem_type, JSON.stringify(telemetries[i].data)]);
                  }
                }
            }
        telemTable.draw();
    });
}

function toggleMonkeyEnabled(event, state) {
    if (event.type != "switchChange") {
        return;
    }
    if (state) {
        reviveMonkey();
    }
    else {
        killMonkey();
    }
}


function killMonkey() {
    var curr_config = monkeyCfg.getValue();
    curr_config.alive = false;
    monkeyCfg.setValue(curr_config);
    updateMonkeyConfig();
}

function reviveMonkey() {
    var curr_config = monkeyCfg.getValue();
    curr_config.alive = true;
    monkeyCfg.setValue(curr_config);
    updateMonkeyConfig();
}

function toggleFocusOnNode() {
    if (focusedOnNode) {
        network.zoomExtent({duration:0});
        focusedOnNode = false;
    }
    else {
        selectNode(undefined, true);
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
                BootstrapDialog.show({
                    title: "Update New Monkeys Config",
                    message: "New monkeys config successfully updated!"
                });
            },
            error : function(jqXHR, textStatus, errorThrown) {
                // log the error to the console
                console.log("The following error occured: " + textStatus, errorThrown);
                BootstrapDialog.show({
                    title: "Update New Monkeys Config",
                    message: "The following error occured: " + textStatus
                });
            },
            complete : function() {
                console.log("Sending new monkeys config update...");
            }
        });
}

function loadMonkeyConfig() {
    var node = network.getSelectedNodes();

    if(node.length != 1) {
        return;
    }

    var monkey = getMonkey(node[0]);

    monkeyCfg.setValue(monkey.config);
}

function updateMonkeyConfig() {
    var node = network.getSelectedNodes();
    if(node.length != 1) {
        return;
    }

    var monkey = getMonkey(node[0]);

    var curr_config = monkeyCfg.getValue();

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
                console.log("Monkey config successfully updated! (" + monkey.hostname + ")");
                selectNode(monkey.hostname, false);
                BootstrapDialog.show({
                    title: "Update Monkey Config",
                    message: "Monkey config successfully updated! (" + monkey.hostname + ")"
                    });
            },
            error : function(jqXHR, textStatus, errorThrown) {
                // log the error to the console
                console.log("The following error occured: " + textStatus, errorThrown);
                BootstrapDialog.show({
                    title: "Update Monkey Config",
                    message: "The following error occured: " + textStatus
                    });
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


function resetDB() {
    if (confirm('Are you sure you want to empty the database?')) {
        $.ajax({
            headers : {
                'Accept' : 'application/json',
            },
            url : '/api?action=reset',
            type : 'GET',
            success : function(response, textStatus, jqXhr) {
                console.log("DB was successfully reset!");
                location.reload();
            },
            error : function(jqXHR, textStatus, errorThrown) {
                // log the error to the console
                console.log("The following error occured: " + textStatus, errorThrown);
                BootstrapDialog.show({
                    title: "Reset DB",
                    message: "The following error occured: " + textStatus
                });
            },
            complete : function() {
                console.log("Trying to reset DB...");
            }
        });
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
    return null;
}

function getMonkeyByIP(ip) {
    for (var i = 0; i < monkeys.length; i++) {
            var monkey = monkeys[i];
            for (var j = 0; j< monkey.ip_addresses.length; j++) {
                if (monkey.ip_addresses[j] == ip) {
                    return monkey;
                }
            }
    }
    return null;
}

function getScannedByIP(ip) {
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
            return edges[i];
        }
    }
}

function removeEdge(link) {
    for (var i = 0; i < edges.length; i++) {
        var from = edges[i].from;
        var to = edges[i].to;
        var type = edges[i].type;
        if (from == link[0] && to == link[1] && type == link[2]) {
            edges.splice(i, 1);
            return true;
        }
    }
    return false;
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
