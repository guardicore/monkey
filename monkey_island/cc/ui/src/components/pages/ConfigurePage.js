import React from 'react';
import Form from 'react-jsonschema-form';
import {Col, Nav, NavItem} from 'react-bootstrap';

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
        selectedSection: 'basic'
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
        this.props.onStatusChange();
      });
  };

  setSelectedSection = (key) => {
    this.setState({
      selectedSection: key
    });
  };

  render() {
    let displayedSchema = this.state.schema["properties"][this.state.selectedSection];
    displayedSchema["definitions"] = this.state.schema["definitions"];
    return (
      <Col xs={8}>
        <h1 className="page-title">Monkey Configuration</h1>

        <Nav bsStyle="tabs" justified
             activeKey={this.state.selectedSection} onSelect={this.setSelectedSection}
             style={{'marginBottom': '2em'}}>
          {this.state.sections.map(section =>
            <NavItem key={section.key} eventKey={section.key}>{section.title}</NavItem>
          )}
        </Nav>

        { this.state.selectedSection ?
          <Form schema={displayedSchema}
                formData={this.state.configuration}
                onSubmit={this.onSubmit}/>
          : ''}

        <div className="alert alert-info">
          <i className="glyphicon glyphicon-info-sign" style={{'marginRight': '5px'}}/>
          This configuration will only apply to new infections.
        </div>

        { this.state.saved ?
          <p>Configuration saved successfully.</p>
          : ''}
      </Col>
    );
  }
}

export default ConfigurePageComponent;
