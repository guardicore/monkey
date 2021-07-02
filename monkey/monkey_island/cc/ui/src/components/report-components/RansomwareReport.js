import React from 'react';

import ReportHeader, {ReportTypes} from './common/ReportHeader';
import ReportLoader from './common/ReportLoader';

class RansomwareReport extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
        report: props.report
    };
  }

  stillLoadingDataFromServer() {
    return Object.keys(this.state.report).length === 0;
  }

  generateReportContent() {
    return (
        <div>
          <p>
            This report shows information about the ransomware simulation run by Infection Monkey.
          </p>
        </div>
    )
  }

  render() {
    let content = {};
    if (this.stillLoadingDataFromServer()) {
        content = <ReportLoader loading={true}/>;
    } else {
      content = <div> {this.generateReportContent()}</div>;
    }
    return (
    <div className='report-page'>
      <ReportHeader report_type={ReportTypes.ransomware}/>
      <hr/>
      {content}
     </div>)
  }
}

export default RansomwareReport;
