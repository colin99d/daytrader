import React, { Component } from "react";

type formOptions = "username" | "password" | "first_name" | "last_name" | "email" | "password2"

type SignupState = {
    password: string,
    password2: string,
    username: string,
    first_name: string,
    last_name: string,
    email: string,
    message: string
}

type SignupProps = {
    handleSignup: (e: any, data:SignupState) => void
    handleClick: (arg: "login") => void
}


class SignupForm extends Component<SignupProps, SignupState> {
    constructor(props: any) {
        super(props);
        this.state = {
            password: '',
            password2: '',
            username: '',
            first_name: '',
            last_name: '',
            email: '',
            message: ''
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
      }

    handleChange(e:any, formKey:formOptions) {this.setState({...this.state, [formKey]: e.target.value})}

    handleClick(e:any) {
      if (this.state.username == "") {
        this.setState({message: "Please enter a username."})
      } else if (this.state.first_name == "") {
        this.setState({message: "Please enter a first name."})
      } else if (this.state.last_name == "") {
        this.setState({message: "Please enter a last name."})
      } else if (this.state.email == "") {
        this.setState({message: "Please enter an email."})
      } else if (this.state.password == "") {
        this.setState({message: "Please enter an password."})
      } else if (this.state.password != this.state.password2) {
        this.setState({message: "Passwords do not match"})
      } else {
        this.props.handleSignup(e, this.state)
      }
    }

    
    
    render() {
      return (
        <div className="min-h-screen bg-gray-100 flex flex-col">
        <div className="p-10 xs:p-0 mx-auto md:w-full md:max-w-md">
          <h1 className="font-bold text-center text-2xl mb-3">Signup</h1>  
          <p className="text-center text-red-500">{this.state.message}</p>
          <div className="bg-white shadow w-full rounded-lg divide-y divide-gray-200">
            <div className="px-5 py-7">
              <label className="font-semibold text-sm text-gray-600 pb-1 block">Username</label>
              <input type="text" value={this.state.username} onChange={(e) => {this.handleChange(e, "username")}} className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full" />

              <label className="font-semibold text-sm text-gray-600 pb-1 block">First Name</label>
              <input type="text" value={this.state.first_name} onChange={(e) => {this.handleChange(e, "first_name")}} className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full" />

              <label className="font-semibold text-sm text-gray-600 pb-1 block">Last Name</label>
              <input type="text" value={this.state.last_name} onChange={(e) => {this.handleChange(e, "last_name")}} className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full" />

              <label className="font-semibold text-sm text-gray-600 pb-1 block">Email</label>
              <input type="email" value={this.state.email} onChange={(e) => {this.handleChange(e, "email")}} className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full" />

              <label className="font-semibold text-sm text-gray-600 pb-1 block">Password</label>
              <input type="password" value={this.state.password} onChange={(e) => {this.handleChange(e, "password")}} className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full" />

              <label className="font-semibold text-sm text-gray-600 pb-1 block">Password (verfiy)</label>
              <input type="password" value={this.state.password2} onChange={(e) => {this.handleChange(e, "password2")}} className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full" />

              <button onClick={e => this.handleClick(e)} type="button" className="transition duration-200 bg-blue-500 hover:bg-blue-600 focus:bg-blue-700 focus:shadow-sm focus:ring-4 focus:ring-blue-500 focus:ring-opacity-50 text-white w-full py-2.5 rounded-lg text-sm shadow-sm hover:shadow-md font-semibold text-center inline-block">Login</button>
            </div>
              <div className="py-5">
              <div className="grid grid-cols-2 gap-1">
                <div className="text-center sm:text-left whitespace-nowrap">
                  <button className="transition duration-200 mx-5 px-5 py-4 cursor-pointer font-normal text-sm rounded-lg text-gray-500 hover:bg-gray-100 focus:outline-none focus:bg-gray-200 focus:ring-2 focus:ring-gray-400 focus:ring-opacity-50 ring-inset">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4 inline-block align-text-top">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
                      </svg>
                      <span className="inline-block ml-1">Forgot Password</span>
                  </button>
                </div>
                <div className="text-center sm:text-right whitespace-nowrap">
                  <button className="transition duration-200 mx-5 px-5 py-4 cursor-pointer font-normal text-sm rounded-lg text-gray-500 hover:bg-gray-100 focus:outline-none focus:bg-gray-200 focus:ring-2 focus:ring-gray-400 focus:ring-opacity-50 ring-inset">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4 inline-block align-text-bottom	">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                      <span className="inline-block ml-1">Help</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div className="py-5">
          <div className="grid grid-cols-2 gap-1">
            <div className="text-center sm:text-left whitespace-nowrap font-normal rounded-lg text-gray-500">
              <span className="inline-block ml-1">Already have an account? {' '}
                <a onClick={() => this.props.handleClick("login")} className="underline cursor-pointer">Login</a>
              </span>
            </div>
          </div>
        </div>
        </div>
        </div>
      );
    }
  }
  
  export default SignupForm;