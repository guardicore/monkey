import AuthComponent from './AuthComponent';
import React from 'react';

export class Response {
  body: any
  status: number

  constructor(body: any, status: number) {
    this.body = body
    this.status = status
  }
}

export enum APIEndpoint {
  agents = '/api/agents',
  machines = '/api/machines',
  nodes = '/api/nodes',
  agentEvents = '/api/agent-events',
  mode = '/api/island/mode',
  manual_exploitation = '/api/exploitations/manual',
  monkey_exploitation = '/api/exploitations/monkey',
  telemetry = '/api/telemetry',
  stolenCredentials = '/api/propagation-credentials/stolen-credentials'
}

class IslandHttpClient extends AuthComponent {
  put(endpoint: string, contents: any): Promise<Response> {
    let status = null;
    return this.authFetch(endpoint,
      {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(contents)
      })
      .then(res => {
        status = res.status;
        return res
      })
      .then(res => new Response(res, status));
  }

  get(endpoint: APIEndpoint, args: Record<string, any>={}): Promise<Response> {
    let status = null;
    let params = new URLSearchParams(args);
    let url = String(endpoint);
    if(params.toString() !== ''){
      url = endpoint + '?' + params;
    }
    return this.authFetch(url)
      .then(res => {
        status = res.status;
        return res.json()
      })
      .then(res => new Response(res, status));
  }
}

export default new IslandHttpClient();
