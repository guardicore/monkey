import React from 'react';
import ReactTable from 'react-table';
import marked from 'marked';


class MitigationsComponent extends React.Component {

  constructor(props) {
    super(props);
    if (typeof this.props.mitigations !== 'undefined' && this.props.mitigations.length > 0){
      this.state = {mitigations: this.props.mitigations};
    } else {
      this.state = {mitigations: null}
    }
  }

  static createRows(descriptions, references) {
    let rows = [];
    for(let i = 0; i < descriptions.length; i++){
      rows[i] = {'description': descriptions[i], 'reference': references[i]};
    }
    return rows;
  }

  static parseDescription(description) {
    const citationRegex = /\(Citation:.*\)/gi;
    const emptyLineRegex = /^\s*[\r\n]/gm;
    description = description.replace(citationRegex, '');
    description = description.replace(emptyLineRegex, '');
    description = marked(description);
    return description;
  }

  static getMitigations() {
    return ([{
      Header: 'Mitigations',
      style: {'text-align': 'left'},
      columns: [
        { id: 'name',
          accessor: x => this.getMitigationName(x.name, x.url),
          width: 200},
        { id: 'description',
          accessor: x => (<div dangerouslySetInnerHTML={{__html: this.parseDescription(x.description)}} />),
          style: {'whiteSpace': 'unset'}}
      ]
    }])
  }

  static getMitigationName(name, url) {
    if(url){
      return (<a href={url} rel="noopener noreferrer" target={'_blank'}>{name}</a>)
    } else {
      return (<p>{name}</p>)
    }
  }


  render() {
    return (
      <div>
        <br/>
        {this.state.mitigations ?
          <ReactTable
            columns={MitigationsComponent.getMitigations()}
            data={this.state.mitigations}
            showPagination={false}
            defaultPageSize={this.state.mitigations.length}
            className={'attack-mitigation'}
          /> : ''}
      </div>
    );
  }
}

export default MitigationsComponent;
