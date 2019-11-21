import React, {Fragment} from 'react';
import AuthComponent from '../AuthComponent';
import ReportHeader, {ReportTypes} from './common/ReportHeader';
import ReportLoader from './common/ReportLoader';
import PrintReportButton from './common/PrintReportButton';
import SummarySection from './zerotrust/SummarySection';
import FindingsSection from './zerotrust/FindingsSection';
import PrinciplesSection from './zerotrust/PrinciplesSection';

class ZeroTrustReportPageComponent extends AuthComponent {

  constructor(props) {
    super(props);
    this.state = this.props.report
  }

  componentDidUpdate(prevProps) {
    if (this.props.report !== prevProps.report) {
     this.setState(this.props.report)
    }
  }

  render() {
    let content;
    if (this.stillLoadingDataFromServer()) {
      content = <ReportLoader loading={true}/>;
    } else {
      content = <div id="MainContentSection">
        <SummarySection allMonkeysAreDead={this.state.allMonkeysAreDead} pillars={this.state.pillars}/>
        <PrinciplesSection principles={this.state.principles}
                           pillarsToStatuses={this.state.pillars.pillarsToStatuses}/>
        <FindingsSection pillarsToStatuses={this.state.pillars.pillarsToStatuses} findings={this.state.findings}/>
      </div>;
    }

    return (
      <Fragment>
        <div style={{marginBottom: '20px'}}>
          <PrintReportButton onClick={() => {
            print();
          }}/>
        </div>
        <div className="report-page">
          <ReportHeader report_type={ReportTypes.zeroTrust}/>
          <hr/>
          {content}
        </div>
        <div style={{marginTop: '20px'}}>
          <PrintReportButton onClick={() => {
            print();
          }}/>
        </div>
      </Fragment>
    )
  }

  stillLoadingDataFromServer() {
    return typeof this.state.findings === 'undefined'
      || typeof this.state.pillars === 'undefined'
      || typeof this.state.principles === 'undefined';
  }


}

export default ZeroTrustReportPageComponent;
