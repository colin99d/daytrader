import React, { Component } from "react";

type ForumProps = {
    text: string,
  }

class Forum extends Component<ForumProps, {}> {

    render() {
      return (
        <div className="flex flex-row py-4 px-2 items-center border-b-2">
        <div className="w-1/4">
            <img src="https://source.unsplash.com/otT2199XwI8/600x600" className="object-cover h-12 w-12 rounded-full" alt=""/>
        </div>
        <div className="w-full">
            <div className="text-lg font-semibold">Everest Trip 2021</div>
            <span className="text-gray-500">Hi Sam, Welcome</span>
        </div>
        
        </div>
  )
}
}

type MessageProps = {
    text: string,
    user: boolean,
  }

class Message extends Component<MessageProps, {}> {

    render() {
        let firstDiv = this.props.user ? "justify-end" : "justify-start"
        let secondDiv = this.props.user ? "mr-2  bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl" : "ml-2 bg-gray-400 rounded-br-3xl rounded-tr-3xl rounded-tl-xl"
      return (
        
        <div className={"flex mb-4 " + firstDiv}>
            <div className={"text-white py-3 px-4 " + secondDiv}>
            {this.props.text}
            </div>
        </div>
  )
}
}

type ChatState = {
    roomName: string
}


class Chat extends Component<{}, ChatState> {
    constructor(props: any) {
        super(props);
        this.state = {
            roomName: ''
        };
        this.handleChange = this.handleChange.bind(this);
      }

    handleChange(e:any, formKey: "roomName") {this.setState({...this.state, [formKey]: e.target.value})}

    render() {
      return (
        <div className="mx-auto shadow-lg rounded-lg mt-1 h-full">
            <div className="flex flex-row justify-between bg-white h-full">
            <div className="flex flex-col w-2/5 border-r-2 overflow-y-auto">
                <div className="border-b-2 py-4 px-2">
                <input value={this.state.roomName} onChange={(e) => {this.handleChange(e, "roomName")}} type="text" placeholder="search chatting" className="py-2 px-2 border-2 border-gray-200 rounded-2xl w-full"/>
                <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Submit</button>
                </div>

                <Forum text={'ur mom'}/>

            </div>
            <div className="w-full px-5 flex flex-col justify-between">
                <div className="flex flex-col mt-5">
                    <Message text={'Hello how is it going today?'} user={true}/>
                    <Message text={'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat'} user={false} />
                </div>
                <input className="w-full bg-gray-300 py-5 px-3 rounded-xl mb-20" type="text"/>
                </div>
            </div>
            </div>
          
       
  )
}
}

export default Chat;