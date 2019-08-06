import React, {Component} from "react";
import ReactTable from "react-table";
import {Button} from "react-bootstrap";
import {EventsModal} from "./EventsModal";

function PillarLabel(props) {
  return <span className="label label-primary" style={{margin: '2px'}}>{props.pillar}</span>
}


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
        <p style={{margin: '5px'}}>
          <Button className="btn btn-danger btn-lg center-block"
                  onClick={this.show}>
            Show Events
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
          return <ul>{listItems}</ul>
        }
      },
      { Header: 'Events', id:"events",
        accessor: x => {
          return <EventsAndButtonComponent events={x.events}/>;
        }
      }
    ]
  }
];

const pageSize = 10;

class ZeroTrustReportFindingsTable extends Component {
  render() {
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
}


export default ZeroTrustReportFindingsTable;
