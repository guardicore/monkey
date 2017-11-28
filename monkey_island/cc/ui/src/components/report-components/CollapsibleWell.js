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
    return (
      <div>
        <a onClick={() => this.setState({ open: !this.state.open })}>
          Read More...
        </a>
        <Collapse in={this.state.open}>
          <div>
            <Well style={{margin: '10px'}}>
              {this.props.children}
            </Well>
          </div>
        </Collapse>
      </div>
    );
  }
}

export default CollapsibleWellComponent;
