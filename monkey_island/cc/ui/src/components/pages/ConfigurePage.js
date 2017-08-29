import React from 'react';
import Form from 'react-jsonschema-form';
import {Col} from 'react-bootstrap';

class ConfigurePageComponent extends React.Component {
  constructor(props) {
    super(props);

    // set schema from server
    this.state = {
      schema: {},
      configuration: {},
      saved: false
    };
  }

  componentDidMount() {
    fetch('/api/configuration')
      .then(res => res.json())
      .then(res => this.setState({
        schema: res.schema,
        configuration: res.configuration
      }));
  }

  onSubmit = ({formData}) => {
    fetch('/api/configuration',
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(formData)
      })
      .then(res => res.json())
      .then(res => {
        this.setState({
          saved: true,
          schema: res.schema,
          configuration: res.configuration
        });
      });
  };

  render() {
    return (
      <Col xs={8}>
        <h1 className="page-title">Monkey Configuration</h1>
        <div className="alert alert-info">
          <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
          This configuration will only apply on new infections.
        </div>
        <Form schema={this.state.schema}
              formData={this.state.configuration}
              onSubmit={this.onSubmit}/>
        { this.state.saved ?
          <p>Configuration saved successfully.</p>
          : ''}
      </Col>
    );
  }
}

export default ConfigurePageComponent;
