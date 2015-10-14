const jsonFile = "/api/monkey";
var monkeys = null;
var generationDate = null;

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

    var data = {
        nodes: createNodes(),
        edges: createEdges()
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
                nodes.push(createNode(new_monkeys[i]));
            }
        }

        if(new_monkeys.length > 0)
        {
            network.setData({nodes: nodes, edges: createEdges()});
        }

        window.setTimeout(updateMonkeys, 10000);
    });    
}

/**
 * Create the nodes used by vis.js
 */
function createNodes() {
    for (var i = 0; i < monkeys.length; i++) {
        var monkey = monkeys[i];

        nodes.push(createNode(monkey));
    }
    return nodes;
}


function createNode(monkey) {
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

function createEdges() {
    for (var i = 0; i < monkeys.length; i++) {
        var monkey = monkeys[i];
        if(monkey.parent != monkey.guid) {
            parent = getMonkeyByGuid(monkey.parent);

            if(parent && !edgeExists([parent.id, monkey.id])) {
                edges.push({from: parent.id, to: monkey.id, arrows:'middle'});
            }
        }
    }

    return edges;
}


/**
 * Builds node description
 */
function buildMonkeyDescription(monkey) {
    var html =
        "<label>Name:</label> " + monkey.hostname + "</br>" +
        "<label>Description:</label> " + monkey.description + "</br>" +
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
        if ((from == link[0] && to == link[1]) ||
            (from == link[1] && to == link[0])) {
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
