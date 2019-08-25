import React from 'react';
import {Button, Col} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import ReportHeader, {ReportTypes} from "../report-components/common/ReportHeader";
import PillarGrades from "../report-components/zerotrust/PillarGrades";
import PillarLabel from "../report-components/zerotrust/PillarLabel";
import ResponsiveVennDiagram from "../report-components/zerotrust/venn-components/ResponsiveVennDiagram";
import FindingsTable from "../report-components/zerotrust/FindingsTable";
import {SinglePillarRecommendationsStatus} from "../report-components/zerotrust/SinglePillarRecommendationsStatus";

let mockup = [
    {
        "Conclusive": 4,
        "Inconclusive": 0,
        "Positive": 1,
        "Unexecuted": 2,
        "pillar": "Data"
    },
    {
        "Conclusive": 0,
        "Inconclusive": 5,
        "Positive": 0,
        "Unexecuted": 2,
        "pillar": "People"
    },
    {
        "Conclusive": 0,
        "Inconclusive": 0,
        "Positive": 6,
        "Unexecuted": 3,
        "pillar": "Networks"
    },
    {
        "Conclusive": 2,
        "Inconclusive": 0,
        "Positive": 1,
        "Unexecuted": 1,
        "pillar": "Devices"
    },
    {
        "Conclusive": 0,
        "Inconclusive": 0,
        "Positive": 0,
        "Unexecuted": 0,
        "pillar": "Workloads"
    },
    {
        "Conclusive": 0,
        "Inconclusive": 2,
        "Positive": 0,
        "Unexecuted": 0,
        "pillar": "Visibility & Analytics"
    },
    {
        "Conclusive": 0,
        "Inconclusive": 0,
        "Positive": 0,
        "Unexecuted": 0,
        "pillar": "Automation & Orchestration"
    }
];

class ZeroTrustReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);

    this.state = {
      allMonkeysAreDead: false,
      runStarted: false
    };
  }

  render() {
    let res;
    // Todo move to componentDidMount
    this.getZeroTrustReportFromServer(res);

    const content = this.generateReportContent();

    return (
      <Col xs={12} lg={10}>
        <h1 className="page-title no-print">5. Zero Trust Report</h1>
        <div style={{'fontSize': '1.2em'}}>
          {content}
        </div>
      </Col>
    );
  }

  generateReportContent() {
    let content;

    if (this.stillLoadingDataFromServer()) {
      content = "Still empty";
    } else {
      const pillarsSection = <div>
        <h2>Pillars Overview</h2>
        <PillarGrades pillars={this.state.pillars}/>
      </div>;

      const recommendationsSection = <div><h2>Recommendations Status</h2>
        {
          this.state.recommendations.map((recommendation) =>
            <SinglePillarRecommendationsStatus
              key={recommendation.pillar}
              pillar={recommendation.pillar}
              recommendationStatus={recommendation.recommendationStatus}/>
          )
        }
      </div>;

      const findingSection = <div><h2>Findings</h2>
        <FindingsTable findings={this.state.findings}/></div>;

      content = <div>
        {pillarsSection}
        {recommendationsSection}
        {findingSection}
      </div>;
    }

    return (
      <div>
        <div className="text-center no-print" style={{marginBottom: '20px'}}>
          <Button bsSize="large" onClick={() => {
            this.print();
          }}><i className="glyphicon glyphicon-print"/> Print Report</Button>
        </div>
        <div className="report-page">
          <ReportHeader report_type={ReportTypes.zeroTrust}/>
          <hr/>
          {content}
          <hr/>
          <pre>{JSON.stringify(this.state.pillars, undefined, 2)}</pre>
          <br/>
          <ResponsiveVennDiagram pillarsGrades={mockup} />
          <pre>{JSON.stringify(this.state.recommendations, undefined, 2)}</pre>
          <br/>
          <pre>{JSON.stringify(this.state.findings, undefined, 2)}</pre>
        </div>
      </div>
    )
  }

  stillLoadingDataFromServer() {
    return typeof this.state.findings === "undefined" || typeof this.state.pillars === "undefined" || typeof this.state.recommendations === "undefined";
  }

  print() {
    alert("unimplemented");
  }

  getZeroTrustReportFromServer() {
    let res;
    this.authFetch('/api/report/zero_trust/findings')
      .then(res => res.json())
      .then(res => {
        this.setState({
          findings: res
        });
      });
    this.authFetch('/api/report/zero_trust/recommendations')
      .then(res => res.json())
      .then(res => {
        this.setState({
          recommendations: res
        });
      });
    this.authFetch('/api/report/zero_trust/pillars')
      .then(res => res.json())
      .then(res => {
        this.setState({
          pillars: res
        });
      });
  }
}

export default ZeroTrustReportPageComponent;
