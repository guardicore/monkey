import React from 'react';
import {Collapse, Well} from 'react-bootstrap';

class CollapsibleWellComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: false
    };
  }

  render() {
    let well =
      (
        <Well style={{margin: '10px'}}>
          {this.props.children}
        </Well>
      );

    return (
      <div>
        <div className="no-print">
          <a onClick={() => this.setState({open: !this.state.open})}>
            Read More...
          </a>
          <Collapse in={this.state.open}>
            <div>
              {well}
            </div>
          </Collapse>
        </div>
        <div className="force-print" style={{display: 'none'}}>
          {well}
        </div>
      </div>
    );
  }
}

export default CollapsibleWellComponent;
