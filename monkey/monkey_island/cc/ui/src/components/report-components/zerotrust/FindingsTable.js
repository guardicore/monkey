import React, {Component} from "react";
import ReactTable from "react-table";
import {Button} from "react-bootstrap";
import {EventsModal} from "./EventsModal";
import FileSaver from "file-saver";
import {PillarLabel} from "./PillarLabel";


class EventsAndButtonComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      show: false
    }
  }

  hide = () => {
    this.setState({show: false});
  };

  show = () => {
    this.setState({show: true});
  };

  render() {
    return (
      <div>
        <EventsModal events={this.props.events} showEvents={this.state.show} hideCallback={this.hide}/>
        <p style={{margin: '1px'}}>
          <Button className="btn btn-info btn-lg center-block"
                  onClick={this.show}>
            Show Events
          </Button>
          <Button className="btn btn-primary btn-lg center-block"
                  onClick={() => {
                    const content = JSON.stringify(this.props.events, null, 2);
                    const blob = new Blob([content], {type: "text/plain;charset=utf-8"});
                    FileSaver.saveAs(blob, this.props.exportFilename+".json");
                  }}
                >
            Export Events
          </Button>
        </p>
      </div>
    );
  }

}

const columns = [
  {
    Header: 'Findings',
    columns: [
      { Header: 'Test', accessor: 'test',
        style: {'whiteSpace': 'unset'}  // This enables word wrap
      },
      { Header: 'Pillars', id: "pillars",
        accessor: x => {
          const pillars = x.pillars;
          const listItems = pillars.map((pillar) =>
            <li key={pillar}><PillarLabel pillar={pillar}/></li>
          );
          return <ul>{listItems}</ul>;
        }
      },
      { Header: 'Events', id:"events",
        accessor: x => {
          return <EventsAndButtonComponent events={x.events} exportFilename={"Events_" + x.test}/>;
        }
      }
    ]
  }
];

const pageSize = 10;

class FindingsTable extends Component {
  render() {
    if (this.props.findings.length > 0) {
      let defaultPageSize = this.props.findings.length > pageSize ? pageSize : this.props.findings.length;
      let showPagination = this.props.findings.length > pageSize;

      return (
        <div>
          <ReactTable
            columns={columns}
            data={this.props.findings}
            showPagination={showPagination}
            defaultPageSize={defaultPageSize}
          />
        </div>
      );
    }
    else { return (<div><pre>BAYAZ</pre></div>);}
  }
}


export default FindingsTable;
