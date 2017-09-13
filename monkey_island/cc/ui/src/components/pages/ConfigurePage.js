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
      saved: false,
      sections: [],
      selectedSection: ''
    };
  }

  componentDidMount() {
    fetch('/api/configuration')
      .then(res => res.json())
      .then(res => this.setState({
        schema: res.schema,
        configuration: res.configuration,
        sections: Object.keys(res.schema.properties)
          .map(key => {
            return {key: key, title: res.schema.properties[key].title}
          }),
        selectedSection: 'monkey'
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

  setSelectedSection = (event) => {
    this.setState({
      selectedSection: event.target.value
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

        <select value={this.state.selectedSection} onChange={this.setSelectedSection}
                className="form-control input-lg" style={{'margin-bottom': '1em'}}>
          {this.state.sections.map(section =>
            <option value={section.key}>{section.title}</option>
          )}
        </select>

        { this.state.selectedSection ?
          <Form schema={this.state.schema.properties[this.state.selectedSection]}
                formData={this.state.configuration}
                onSubmit={this.onSubmit}/>
          : ''}

        { this.state.saved ?
          <p>Configuration saved successfully.</p>
          : ''}
      </Col>
    );
  }
}

export default ConfigurePageComponent;
