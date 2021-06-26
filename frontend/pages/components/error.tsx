import React, { Component } from "react";

class Error extends Component<{},{}> {
    
  render() {
    return (
        <div>
            <h1>You have reached this page in error</h1>
            <p>Contact your admin for help</p>
        </div>
    );
  }
}

export default Error;