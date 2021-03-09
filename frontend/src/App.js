import React, { Component } from 'react';
import logo from './logo.svg';
import LinkForm from "./components/LinkForm.js"
import './App.css';

// TODO make a components that renders the links saved in the app : GET /api/v1/link
class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1>Welcome to React</h1>
        </div>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <LinkForm/>
      </div>
    );
  }
}

export default App;
