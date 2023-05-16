const POLYMORPHISM_SCHEMA = {
  'title': 'Polymorphism',
  'properties': {
    'enabled': {
      'title': 'Emulate polymorphism',
      'type': 'boolean',
      'default': false,
      'description': 'Emulate polymorphic (or metamorphic) malware by ' +
                     'modifying the Agent binary before propagation.'
    }
  }
}

export default POLYMORPHISM_SCHEMA;
