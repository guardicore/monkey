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
      <h4>Statuses</h4>
      <ul style={{listStyle: "none"}}>
        <li>
          <div style={{display: "inline-block"}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.failed}/>
          </div>
          {"\t"}Some tests failed; the monkeys found something wrong.
        </li>
        <li>
          <div style={{display: "inline-block"}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.inconclusive}/>
          </div>
          {"\t"}The test ran; manual verification is required to determine the results.
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
      Some of the tests can be activated using the <NavLink to="/configuration"><u>configuration</u></NavLink>.
    </div>;
  }
}

export default ZeroTrustReportLegend;
