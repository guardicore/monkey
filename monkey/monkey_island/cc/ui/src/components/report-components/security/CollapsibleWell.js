import React from 'react';
import {Button, Collapse, Card} from 'react-bootstrap';

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
        <Card body>
          {this.props.children}
        </Card>
      );

    return (
      <div>
        <div className="no-print">
          <Button onClick={() => this.setState({open: !this.state.open})}
                  variant="link">
            Read More...
          </Button>
          <Collapse in={this.state.open} style={{margin: '10px'}}>
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
