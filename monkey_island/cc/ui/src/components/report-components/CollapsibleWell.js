import React from 'react';
import {Button, Collapse, Well} from 'react-bootstrap';

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
          <Button onClick={() => this.setState({open: !this.state.open})} bsStyle="link">
            Read More...
          </Button>
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
