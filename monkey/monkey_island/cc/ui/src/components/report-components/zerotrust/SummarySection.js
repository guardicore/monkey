import React, {Component} from "react";
import {Col, Grid, Row} from "react-bootstrap";
import MonkeysStillAliveWarning from "../common/MonkeysStillAliveWarning";
import PillarsOverview from "./PillarOverview";
import ZeroTrustReportLegend from "./ReportLegend";
import * as PropTypes from "prop-types";

export default class SummarySection extends Component {
  render() {
    return <div id="summary-section">
      <h2>Summary</h2>
      <Grid fluid={true}>
        <Row>
          <Col xs={12} sm={12} md={12} lg={12}>
            <MonkeysStillAliveWarning allMonkeysAreDead={this.props.allMonkeysAreDead}/>
            <p>
              Get a quick glance at how your network aligns with the <a href="https://www.forrester.com/report/The+Zero+Trust+eXtended+ZTX+Ecosystem/-/E-RES137210">Zero
              Trust eXtended (ZTX) framework</a>.
            </p>
          </Col>
        </Row>
        <Row className="show-grid">
          <Col xs={8} sm={8} md={8} lg={8}>
            <PillarsOverview pillarsToStatuses={this.props.pillars.pillarsToStatuses}
                             grades={this.props.pillars.grades}/>
          </Col>
          <Col xs={4} sm={4} md={4} lg={4}>
            <ZeroTrustReportLegend/>
          </Col>
        </Row>
      </Grid>
    </div>
  }
}

SummarySection.propTypes = {
  allMonkeysAreDead: PropTypes.bool,
  pillars: PropTypes.object
};
