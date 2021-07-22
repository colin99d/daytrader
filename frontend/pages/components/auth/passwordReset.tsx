import React, { Component } from "react";

type SignupState = {
    email: string,
    message: string,
    response: [string, boolean]
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
            response: ['',null]
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
              this.setState({response: ["Email failed to send",false]})
              throw new Error('Invalid signup attempt');
            }
          })
        .then(json => {
          this.setState({response: ["Email succesfully sent", true]})
        })
        .catch((error) => {
          this.setState({response: ["Email failed to send", false]})
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
      let responseClass:string = this.state.response[1] ? "text-center text-green-500" : "text-center text-red-500"
      return (
        <div className="min-h-screen bg-gray-100 flex flex-col">
        <div className="p-10 xs:p-0 mx-auto md:w-full md:max-w-md">
          <h1 className="font-bold text-center text-2xl mb-3">Password Reset</h1>  
          <p className="text-center text-red-500">{this.state.message}</p>
          <p className={responseClass}>{this.state.response[0]}</p>
          <div className="bg-white shadow w-full rounded-lg divide-y divide-gray-200">
            <div className="px-5 py-7">

              <label className="font-semibold text-sm text-gray-600 pb-1 block">Email</label>
              <input type="email" value={this.state.email} onChange={(e) => {this.handleChange(e)}} className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full" />

              <button onClick={e => this.handleClick(e)} type="button" className="transition duration-200 bg-blue-500 hover:bg-blue-600 focus:bg-blue-700 focus:shadow-sm focus:ring-4 focus:ring-blue-500 focus:ring-opacity-50 text-white w-full py-2.5 rounded-lg text-sm shadow-sm hover:shadow-md font-semibold text-center inline-block">Reset</button>
            </div>
              <div className="py-5">
              <div className="grid grid-cols-2 gap-1">
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