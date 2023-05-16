const POLYMORPHISM_SCHEMA = {
  'title': 'Polymorphism',
  'properties': {
    'randomized_agent_hash': {
      'title': 'Randomize Agent hash',
      'type': 'boolean',
      'default': false,
      'description': 'Emulate the property of polymorphic (or metamorphic) malware that all ' +
                     'copies have unique hashes by modifying the Agent binary before propagation.'
    }
  }
}

export default POLYMORPHISM_SCHEMA;
