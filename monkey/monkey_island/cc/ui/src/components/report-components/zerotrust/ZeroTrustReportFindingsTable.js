import React, {Component} from "react";
import ReactTable from "react-table";
import {Button, Modal} from "react-bootstrap";

class PillarLabel extends Component {
  render() {
    return <span className="label label-primary" style={{margin: '2px'}}>{this.props.pillar}</span>
  }
}

class EventsModal extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <Modal show={this.props.showEvents} onHide={() => this.props.hideCallback()}>
          <Modal.Body>
            <h2><div className="text-center">Events</div></h2>

            <pre>{JSON.stringify(this.props.events)}</pre>

            <div className="text-center">
              <button type="button" className="btn btn-success btn-lg" style={{margin: '5px'}}
                      onClick={() => this.props.hideCallback()}>
                Close
              </button>
            </div>
          </Modal.Body>
        </Modal>
      </div>
    );
  }
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
          return <EventsAndButtonComponent events={x}/>;
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
