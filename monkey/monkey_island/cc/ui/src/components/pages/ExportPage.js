import React from 'react';
import {Col, Button} from 'react-bootstrap';
import AuthComponent from '../AuthComponent';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheck, faCloud, faInfo, faTag} from "@fortawesome/free-solid-svg-icons";
import {Link} from "react-router-dom";

const ExportStatus = {
    BEFORE: "Before",
    SUCCESS: "Success",
    ERROR: "Error",
};

class ExportPageComponent extends AuthComponent {
  exported;
  constructor(props) {
    super(props);

    this.state = {
        exported: ExportStatus.BEFORE
    };
  }

  render() {
    console.log("rendering, cur state is " + JSON.stringify(this.state));
    let statusBox;
    switch(this.state.exported) {
      case ExportStatus.BEFORE:
        statusBox = '';
        break;
      case ExportStatus.ERROR:
        statusBox = (
          <div className="alert alert-danger">
              <FontAwesomeIcon icon={faInfo} style={{'marginRight': '5px'}}/>
              Error while exporting. Check the <Link to="/infection/telemetry">server logs</Link> for more details.
          </div>
        );
        break;
      case ExportStatus.SUCCESS:
        statusBox = (
          <div className="alert alert-success">
              <FontAwesomeIcon icon={faCheck} style={{'marginRight': '5px'}}/>
              Exported successfully.
            </div>
        );
        break;
    }
    return (
      <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 9}} xl={{offset: 2, span: 7}}
           className={'main'}>
        <h1 className="page-title">Export</h1>
        <div style={{'fontSize': '1.2em'}}>
          <p>
            The Monkey Island automatically exports its findings every time a report is generated. However, if you wish to
            manually export, this is the page for you.
          </p>
          <div style={{margin: '20px'}}>
            <ul>
              <li>
            <Button className="btn btn-info btn-lg center-block"
                    onClick={() => {
                      this.export("AWSExporter")
                    }
                    }>
              <FontAwesomeIcon icon={faCloud} style={{'marginRight': '5px'}}/> Export findings to AWS
            </Button>
              </li>
              <br/>
              <li>
              <Button className="btn btn-info btn-lg center-block"
                      onClick={() => {
                        this.export("LabelsExporter")
                      }
                      }>
                <FontAwesomeIcon icon={faTag} style={{'marginRight': '5px'}}/> Export labels to file
              </Button>
              </li>
              </ul>
          </div>
          {statusBox}
        </div>
      </Col>
    );
  }

  export = (exporter) => {
    this.setState({
      exported: false
    });
    return this.authFetch('/api/export/' + exporter)
      .then(res => {
        console.log(res);
        if (res['status'] === 200) {
          this.setState({
            exported: ExportStatus.SUCCESS
          });
        } else {
          console.log("errir");
          this.setState({
            exported: ExportStatus.ERROR
          })
        }
      });
  };
}

export default ExportPageComponent;
