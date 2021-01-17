import React, { Component } from 'react'
import * as BackendAPI from './BackendAPI'
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      admin: [],
      items: [],
    };
  }

  /*********************/
  /* Lifecycle Methods */
  /*********************/

  componentDidMount() {
    BackendAPI.getAdmin().then((admin) => {
      this.setState({admin});
    })

    BackendAPI.getItems().then((items) => {
      this.setState({items})
    })   
  }

  /********************/
  /* API Prep Methods */
  /********************/

  

  /************/
  /** Render **/
  /************/

  render() {

    return (
      <div className="app">
        <h1>Admin</h1>
        <ul>
          {this.state.admin.map(adminItem => <div key={adminItem.text}>{adminItem.text}</div>)}
        </ul>

        <h2>Items</h2>
        <ul>
          {this.state.items.map(item => <div key={item.id}>{item.text}</div>)}
        </ul>
      </div>
    );
  }
}

export default App;
