import React from 'react';

import ReportHeader, {ReportTypes} from './common/ReportHeader';
import ReportLoader from './common/ReportLoader';
import pluralize from 'pluralize'
import FileEncryptionTable from './ransomware/FileEncryptionTable';

import '../../styles/pages/report/RansomwareReport.scss';

class RansomwareReport extends React.Component {

  stillLoadingDataFromServer() {
    return Object.keys(this.props.report).length === 0;
  }

  generateReportContent() {
    return (
      <div>
        {this.getExploitationStats()}
        <FileEncryptionTable tableData={this.props.report.encrypted_files_table} />
      </div>
    )
  }

  getExploitationStats() {
    return (
        <>
          <p>
            This report shows information about the ransomware simulation run by Infection Monkey.
          </p>
          <div>
            <h3 className={'report-section-header'}>
              Propagation
            </h3>
            {this.getScannedVsExploitedStats()}
            {this.getExploitationStatsPerExploit()}
          </div>
        </>
    )
  }

  getScannedVsExploitedStats() {
    let num_scanned = this.props.report.propagation_stats.num_scanned_nodes;
    let num_exploited = this.props.report.propagation_stats.num_exploited_nodes;

    return(
      <p>
        The Monkey discovered <span className='badge badge-warning'>{num_scanned}</span> machines
        and successfully breached <span className='badge badge-danger'>{num_exploited}</span> of them.
      </p>
    )
  }

  getExploitationStatsPerExploit() {
    let exploit_counts = this.props.report.propagation_stats.num_exploited_per_exploit;

    let exploitation_details = [];

    for (let exploit in exploit_counts) {
      let count = exploit_counts[exploit];
      exploitation_details.push(
        <div>
          <span className='badge badge-danger'>{count}</span>&nbsp;
          {pluralize('machine', count)} {pluralize('was', count)} exploited by the&nbsp;
          <span className='badge badge-danger'>{exploit}</span>.
        </div>
      );
    }

    return exploitation_details;
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
