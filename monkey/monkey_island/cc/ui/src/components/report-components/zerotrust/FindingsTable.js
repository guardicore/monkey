import React, {Component, Fragment} from "react";
import PillarLabel from "./PillarLabel";
import PaginatedTable from "../common/PaginatedTable";
import EventsAndButtonComponent from "./EventsAndButtonComponent";


const columns = [
  {
    columns: [
      { Header: 'Pillars', id: "pillars",
        accessor: x => {
          const pillars = x.pillars;
          const pillarLabels = pillars.map((pillar) =>
            <PillarLabel key={pillar.name} pillar={pillar.name} status={pillar.status}/>
          );
          return <div style={{textAlign: "center"}}>{pillarLabels}</div>;
        },
        maxWidth: 200,
        style: {'whiteSpace': 'unset'}
      },
      { Header: 'Finding', accessor: 'test',
        style: {'whiteSpace': 'unset'}  // This enables word wrap
      },

      { Header: 'Events', id:"events",
        accessor: x => {
          return <EventsAndButtonComponent events={x.events} exportFilename={"Events_" + x.test_key}/>;
        },
        maxWidth: 160,
      }
    ]
  }
];

class FindingsTable extends Component {
  render() {
    const data = this.props.findings.map((finding) => {
      const newFinding = JSON.parse(JSON.stringify(finding));
      newFinding.pillars = newFinding.pillars.map((pillar) => {
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
