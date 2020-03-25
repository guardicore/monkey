import React from 'react';
import ReactTable from 'react-table';
import marked from 'marked';


class MitigationsComponent extends React.Component {

  constructor(props) {
    super(props);
    if (typeof this.props.mitigations !== 'undefined'){
      let descriptions = MitigationsComponent.parseDescription(this.props.mitigations.description);
      this.state = {name: this.props.mitigations.name, descriptions: descriptions};
    } else {
      this.state = {name: '', descriptions: []}
    }
  }

  static parseDescription(description){
    const citationRegex = /\(Citation:.*\)/gi;
    const emptyLineRegex = /^\s*[\r\n]/gm;
    description = description.replace(citationRegex, '');
    description = description.replace(emptyLineRegex, '');
    let descriptions = description.split('\n');
    descriptions = descriptions.map(function(paragraph){ return marked(paragraph); });
    return descriptions;
  }

  static getMitigationDescriptions(name) {
    return ([{
      Header: name,
      columns: [
        { id: 'description',
          accessor: x => (<div dangerouslySetInnerHTML={{__html: x}} />),
          style: {'whiteSpace': 'unset'}}
      ]
    }])
  }

  render() {
    return (
      <div>
        <br/>
        {this.state.descriptions.length !== 0 ?
          <ReactTable
            columns={MitigationsComponent.getMitigationDescriptions(this.state.name)}
            data={this.state.descriptions}
            showPagination={false}
            defaultPageSize={this.state.descriptions.length}
          /> : ''}
      </div>
    );
  }
}

export default MitigationsComponent;
