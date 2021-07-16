import React, { Component } from "react";

type SignupState = {
    email: string,
    message: string,
    error: string
}

type SignupProps = {
    handleClick: (arg: "login" | "passwordReset") => void,
    baseUrl: string,
}


class PasswordReset extends Component<SignupProps, SignupState> {
    constructor(props: any) {
        super(props);
        this.state = {
            email: '',
            message: '',
            error: ''
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.submitReset = this.submitReset.bind(this);
      }

    submitReset() {
        fetch(this.props.baseUrl + '/api/password_reset/',  {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({'email':this.state.email})
        })
        .then((response) => {
            if (response.ok) {
              return response.json()
            } else {
              this.setState({error: "Invalid password or username"})
              throw new Error('Invalid signup attempt');
            }
          })
            .then(json => {
              console.log(json)
            });
    }

    handleChange(e:any) {this.setState({email: e.target.value})}

    handleClick(e:any) {
        if (this.state.email == "") {
        this.setState({message: "Please enter an email."})
        } else {
            this.submitReset();
        }
    }

    
    render() {
      return (
        <div className="min-h-screen bg-gray-100 flex flex-col">
        <div className="p-10 xs:p-0 mx-auto md:w-full md:max-w-md">
          <h1 className="font-bold text-center text-2xl mb-3">Password Reset</h1>  
          <p className="text-center text-red-500">{this.state.message}</p>
          <div className="bg-white shadow w-full rounded-lg divide-y divide-gray-200">
            <div className="px-5 py-7">

              <label className="font-semibold text-sm text-gray-600 pb-1 block">Email</label>
              <input type="email" value={this.state.email} onChange={(e) => {this.handleChange(e)}} className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full" />

              <button onClick={e => this.handleClick(e)} type="button" className="transition duration-200 bg-blue-500 hover:bg-blue-600 focus:bg-blue-700 focus:shadow-sm focus:ring-4 focus:ring-blue-500 focus:ring-opacity-50 text-white w-full py-2.5 rounded-lg text-sm shadow-sm hover:shadow-md font-semibold text-center inline-block">Reset</button>
            </div>
              <div className="py-5">
              <div className="grid grid-cols-2 gap-1">
                <div className="text-center sm:text-left whitespace-nowrap">
                  <button className="transition duration-200 mx-5 px-5 py-4 cursor-pointer font-normal text-sm rounded-lg text-gray-500 hover:bg-gray-100 focus:outline-none focus:bg-gray-200 focus:ring-2 focus:ring-gray-400 focus:ring-opacity-50 ring-inset">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4 inline-block align-text-top">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
                      </svg>
                      <span className=""></span>
                      
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
  
  export default PasswordReset;