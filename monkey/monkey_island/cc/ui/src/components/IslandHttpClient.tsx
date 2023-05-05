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
  agent_otp = '/api/agent-otp',
  agents = '/api/agents',
  machines = '/api/machines',
  nodes = '/api/nodes',
  agentEvents = '/api/agent-events',
  mode = '/api/island/mode',
  monkey_exploitation = '/api/exploitations/monkey',
  stolenCredentials = '/api/propagation-credentials/stolen-credentials',
  linuxMasque = '/api/agent-binaries/linux/masque',
  windowsMasque = '/api/agent-binaries/linux/masque'
}

class IslandHttpClient extends AuthComponent {
  put(endpoint: string, contents: any, refreshToken: boolean = false): Promise<Response> {
    let status = null;
    return this.authFetch(endpoint,
      {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(contents)
      },
      refreshToken
    )
      .then(res => {
        status = res.status;
        return res
      })
      .then(res => new Response(res, status));
  }

  get(endpoint: APIEndpoint, args: Record<string, any>={}, refreshToken: boolean = false): Promise<Response> {
    let status = null;
    return this.getBytes(endpoint, args, refreshToken)
      .then(res => {
        status = res.status;
        return res.body.json()
      })
      .then(res => new Response(res, status));
  }

  getBytes(endpoint: APIEndpoint, args: Record<string, any>={}, refreshToken: boolean = false): Promise<Response> {
    let status = null;
    let params = new URLSearchParams(args);
    let url = String(endpoint);
    if(params.toString() !== ''){
      url = endpoint + '?' + params;
    }
    return this.authFetch(url, {}, refreshToken)
      .then(res => {
        status = res.status;
        return res;
      })
      .then(res => new Response(res, status));
  }
}

export default new IslandHttpClient();
