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
      <h4>What is this?</h4>
      <p>
        The Zero Trust eXtended framework categorizes its <b>recommendations</b> into 7 <b>pillars</b>. Infection Monkey
        Zero Trust edition tests some of those recommendations. The <b>tests</b> that the monkey executes
        produce <b>findings</b>. The tests, recommendations and pillars are then granted a <b>status</b> in accordance
        with the tests results.
      </p>
      <h4>Statuses</h4>
      <ul style={{listStyle: "none"}}>
        <li>
          <div style={{display: "inline-block"}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.failed}/>
          </div>
          {"\t"}The test failed; the monkeys found something wrong.
        </li>
        <li>
          <div style={{display: "inline-block"}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.inconclusive}/>
          </div>
          {"\t"}The test was executed, but manual verification is required to determine the results.
        </li>
        <li>
          <div style={{display: "inline-block"}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.passed}/>
          </div>
          {"\t"}This status means the test passed 🙂
        </li>
        <li>
          <div style={{display: "inline-block"}}>
            <StatusLabel showText={true} status={ZeroTrustStatuses.unexecuted}/>
          </div>
          {"\t"}This status means the test wasn't executed. Some of the tests can be activated or deactivated using
          the <NavLink to="/configuration">configuration</NavLink>.
        </li>
      </ul>
    </div>;
  }
}

export default ZeroTrustReportLegend;
