import AuthComponent from "./AuthComponent";
import React from "react";

export class Response{
  body: any
  status: number

  constructor(body: any, status: number) {
    this.body = body
    this.status = status
  }
}

class IslandHttpClient extends AuthComponent {
  put(endpoint: string, contents: any): Promise<Response>{
    let status = null;
    return this.authFetch(endpoint,
      {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(contents)
      })
      .then(res => {status = res.status; return res})
      .then(res => new Response(res, status));
  }

  get(endpoint: string): Promise<Response>{
    let status = null;
    return this.authFetch(endpoint)
      .then(res => {status = res.status; return res.json()})
      .then(res => new Response(res, status));
  }
}

export default new IslandHttpClient();
