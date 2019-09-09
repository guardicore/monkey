import React, {Component} from "react";
import StatusLabel from "./StatusLabel";
import {ZeroTrustStatuses} from "./ZeroTrustPillars";
import {NavLink} from "react-router-dom";
import {Panel} from "react-bootstrap";


class ZeroTrustReportLegend extends Component {
  render() {
    const legendContent = this.getLegendContent();

    return (
      <Panel>
        <Panel.Heading>
          <Panel.Title toggle>
            <h3><i className="fa fa-chevron-down" /> Legend</h3>
          </Panel.Title>
        </Panel.Heading>
        <Panel.Collapse>
          <Panel.Body>
            {legendContent}
          </Panel.Body>
        </Panel.Collapse>
      </Panel>
    );
  }

  getLegendContent() {
    return <div id={this.constructor.name}>
      <ul style={{listStyle: "none"}}>
        <li>
          <div style={{display: "inline-block"}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.failed}/>
          </div>
          {"\t"}At least one of the tests related to this component failed. This means that the Infection Monkey detected an unmet Zero Trust requirement.
        </li>
        <li>
          <div style={{display: "inline-block"}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.inconclusive}/>
          </div>
          {"\t"}At least one of the tests’ results related to this component requires further manual verification.
        </li>
        <li>
          <div style={{display: "inline-block"}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.passed}/>
          </div>
          {"\t"}The test passed, so this is OK 🙂
        </li>
        <li>
          <div style={{display: "inline-block"}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.unexecuted}/>
          </div>
          {"\t"}This status means the test wasn't executed.
        </li>
      </ul>
      <hr />
      To activate more tests, go to the Monkey <NavLink to="/configuration"><u>configuration</u></NavLink> page.n
    </div>;
  }
}

export default ZeroTrustReportLegend;
