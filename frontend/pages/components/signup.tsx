import React, { Component } from "react";

type formOptions = "username" | "password" | "first_name" | "last_name" | "email"

type SignupState = {
    password: string,
    username: string,
    first_name: string,
    last_name: string,
    email: string
}

type SignupProps = {
    handleSignup: (e: any, data:SignupState) => void
}


class SignupForm extends Component<SignupProps, SignupState> {
    constructor(props: any) {
        super(props);
        this.state = {
            password: '',
            username: '',
            first_name: '',
            last_name: '',
            email: '',
        };
        this.handleChange = this.handleChange.bind(this);
      }

    handleChange(e:any, formKey:formOptions) {this.setState({...this.state, [formKey]: e.target.value})}

  
    render() {
      return (
        <form onSubmit={e => this.props.handleSignup(e, this.state)}>
          <h4>Sign Up</h4>
          <label>Username</label>
          <input type="text" value={this.state.username} onChange={(e) => {this.handleChange(e, "username")}}/>
          <label>First Name</label>
          <input type="text" value={this.state.username} onChange={(e) => {this.handleChange(e, "first_name")}}/>
          <label>Last Name</label>
          <input type="text" value={this.state.username} onChange={(e) => {this.handleChange(e, "last_name")}}/>
          <label>Email</label>
          <input type="email" value={this.state.username} onChange={(e) => {this.handleChange(e, "email")}}/>
          <label>Password</label>
          <input type="password" value={this.state.password} onChange={(e) => {this.handleChange(e, "password")}}/>
          <input type="submit" />
        </form>
      );
    }
  }
  
  export default SignupForm;