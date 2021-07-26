import React from 'react';

import ReportHeader, {ReportTypes} from './common/ReportHeader';
import ReportLoader from './common/ReportLoader';
import FileEncryptionTable from './ransomware/FileEncryptionTable';
import LateralMovement from './ransomware/LateralMovement';

import '../../styles/pages/report/RansomwareReport.scss';
import BreachSection from './ransomware/BreachSection';

class RansomwareReport extends React.Component {

  stillLoadingDataFromServer() {
    return Object.keys(this.props.report).length === 0;
  }

  generateReportContent() {
    return (
      <div>
        <BreachSection/>
        <LateralMovement propagationStats={this.props.report.propagation_stats} />
        <FileEncryptionTable tableData={this.props.report.encrypted_files_table} />
      </div>
    )
  }

  render() {
    let content = {};
    if (this.stillLoadingDataFromServer()) {
        content = <ReportLoader loading={true}/>;
    } else {
      content = this.generateReportContent();
    }

    return (
    <div className={`report-page ransomware-report`}>
      <ReportHeader report_type={ReportTypes.ransomware}/>
      <hr/>
      {content}
     </div>)
  }
}

export default RansomwareReport;
