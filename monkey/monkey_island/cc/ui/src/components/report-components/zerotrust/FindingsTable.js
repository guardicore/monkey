import React, {Component} from "react";
import {Button} from "react-bootstrap";
import {EventsModal} from "./EventsModal";
import FileSaver from "file-saver";
import {PillarLabel} from "./PillarLabel";
import PaginatedTable from "../common/PaginatedTable";


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
      { Header: 'Finding', accessor: 'test',
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

class FindingsTable extends Component {
  render() {
    return (
      <PaginatedTable data={this.props.findings} pageSize={10} columns={columns}/>
    );
  }
}


export default FindingsTable;
