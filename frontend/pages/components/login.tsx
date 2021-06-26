import React, { Component } from "react";

type LoginState = {
    password: string,
    username: string,
}

type LoginProps = {
    handleLogin: (e: any, data:LoginState) => void
}


class Login extends Component<LoginProps, LoginState> {
    constructor(props: any) {
        super(props);
        this.state = {
            password: '',
            username: '',
        };
        this.handleChange = this.handleChange.bind(this);
      }
    
    handleChange(e:any, formKey:"username" | "password") {this.setState({...this.state, [formKey]: e.target.value})}

  render() {
    return (
      <form onSubmit={e => this.props.handleLogin(e, this.state)}>
        <h4>Log In</h4>
        <label htmlFor="username">Username</label>
        <input type="text" value={this.state.username} onChange={(e) => {this.handleChange(e, "username")}}/>
        <label htmlFor="password">Password</label>
        <input type="password" value={this.state.password} onChange={(e) => {this.handleChange(e, "password")}}/>
        <input type="submit" />
      </form>
    );
  }
}

export default Login;