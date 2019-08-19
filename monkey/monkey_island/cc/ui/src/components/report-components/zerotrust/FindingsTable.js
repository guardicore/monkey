import React, {Component} from "react";
import PillarLabel from "./PillarLabel";
import PaginatedTable from "../common/PaginatedTable";
import EventsAndButtonComponent from "./EventsAndButtonComponent";


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
            <li key={pillar.name}><PillarLabel pillar={pillar.name} status={pillar.status}/></li>
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
    const data = this.props.findings.map((finding) => {
      const newFinding = finding;
      newFinding.pillars = finding.pillars.map((pillar) => {
        return {name: pillar, status: this.props.pillarsToStatuses[pillar]}
        });
      return newFinding;
    });
    return (
      <PaginatedTable data={data} pageSize={10} columns={columns}/>
    );
  }
}


export default FindingsTable;
