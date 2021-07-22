import React, { Component } from "react";

type algorithm = {
  id: number,
  name: string,
  description: string,
  public: boolean,
  created_at: Date,
}

type user_type = {
  username: string,
  id: number,
  selected_algo: algorithm,
  daily_emails: boolean
}

type HeaderProps = {
    handleClick: (text:string) => void,
    handleLogout: () => void,
    page: string,
    user: user_type,
    baseUrl: string
    updateUser: (object: user_type) => void,
  }

class Header extends Component<HeaderProps, {}> {

  constructor(props: any) {
    super(props);
    this.state = {};
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    fetch(this.props.baseUrl + "/user/update_email",  {
      headers: {Authorization: `Token ${localStorage.getItem('token')}`}
    })
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { error: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then((json) => {
          this.props.updateUser(json);
      })
  }

    render() {
      return (
    <nav className="bg-white shadow h-16 -mt-16">
    <div className="max-w-7xl mx-4 px-2">
      <div className="relative flex justify-between">
        <div className="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
          <div className="flex-shrink-0 flex items-center">
            <img className="hidden sm:block h-8 w-auto" src="https://tailwindui.com/img/logos/workflow-logo-indigo-600-mark-gray-800-text.svg" alt="Workflow" />
          </div>
          <div className="sm:ml-6 sm:flex">
            <a onClick={() => this.props.handleClick("home")} className={this.props.page == "home" ? "border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"}>Dashboard</a>
            <a onClick={() => this.props.handleClick("algorithm")} className={this.props.page == "algorithm" ? "border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"}>Algorithms</a>
            <a onClick={() => this.props.handleClick("chat")} className={this.props.page == "chat" ? "border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"}>Chat</a>
          </div>
        </div>
          <div className="relative inline-block text-left dropdown align-middle mt-3">
            <span className="rounded-md shadow-sm">
              <button className="inline-flex justify-center w-full px-4 py-2 text-sm font-medium leading-5 text-gray-700 transition duration-150 ease-in-out bg-white border border-gray-300 rounded-md hover:text-gray-500 focus:outline-none focus:border-blue-300 focus:shadow-outline-blue active:bg-gray-50 active:text-gray-800" 
              type="button" aria-haspopup="true" aria-expanded="true" aria-controls="headlessui-menu-items-117">
                <span>More</span>
                <svg className="w-5 h-5 ml-2 -mr-1" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd"></path></svg>
                </button>
              </span>
            <div className="opacity-0 invisible dropdown-menu transition-all duration-300 transform origin-top-right -translate-y-2 scale-95">
              <div className="absolute right-0 w-56 mt-2 origin-top-right bg-white border border-gray-200 divide-y divide-gray-100 rounded-md shadow-lg outline-none" aria-labelledby="headlessui-menu-button-1" id="headlessui-menu-items-117" role="menu">
                <div className="px-4 py-3">         
                  <p className="text-sm leading-5">Signed in as</p>
                  <p className="text-sm font-medium leading-5 text-gray-900 truncate">{this.props.user ? this.props.user.username : null} - {this.props.user ? this.props.user.daily_emails ? "Subscribed" : "Not Subscribed" : null}</p>
                </div>
                <div className="py-1">
                  <a onClick={this.handleClick} href="#" tabIndex={1} className="text-gray-700 flex justify-between w-full px-4 py-2 text-sm leading-5 text-left"  role="menuitem">{this.props.user ? this.props.user.daily_emails ? "Unsubscribe" : "Subscribe" : null}</a>
                </div>
                <div className="py-1">
                  <a onClick={this.props.handleLogout} tabIndex={3} className="text-gray-700 flex justify-between w-full px-4 py-2 text-sm leading-5 text-left cursor-pointer"  role="menuitem">Sign out</a></div>
              </div>
            </div>
          </div>
      </div>
    </div>
  </nav>
  )
}
}

export default Header;
