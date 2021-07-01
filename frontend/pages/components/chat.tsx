import React, { Component } from "react";

type ForumProps = {
    text: string,
    changeRoom: (newRoom: string) => void,
  }

class Forum extends Component<ForumProps, {}> {

    render() {
      return (
        <div className="flex flex-row py-4 px-2 items-center border-b-2" onClick={() => this.props.changeRoom(this.props.text)}>
          <div className="w-full">
              <div className="text-lg font-semibold">{this.props.text}</div>
              <span className="text-gray-500"></span>
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

type topic = {
  id: number,
  name: string,
  created_at: Date,
}

type ChatState = {
    roomName: string,
    activeRoom: string,
    messages: string[],
    topics: topic[],
    message: string,
    error: string
}

type ChatProps = {
  baseUrl: string
}


class Chat extends Component<ChatProps, ChatState> {
    constructor(props: any) {
        super(props);
        this.state = {
            roomName: '',
            activeRoom: '',
            messages: [],
            topics: [],
            message: '',
            error: ''
        };
        this.handleChange = this.handleChange.bind(this);
        this.changeRoom = this.changeRoom.bind(this);
      }

    handleChange(e:any, formKey: "roomName" | "message") {this.setState({...this.state, [formKey]: e.target.value})}

    changeRoom(newRoom:string) {
      
      this.setState({activeRoom: newRoom})
      this.getFetch("/api/topics/", "topics");
      let chatSocket = new WebSocket('ws://'+ this.props.baseUrl.replace("http://","")+ '/ws/chat/'+newRoom+'/'+"?token="+localStorage.getItem('token'));
      chatSocket.onmessage = function(e) {
        
        const data = JSON.parse(e.data);
        const messages = this.state.messages;
        messages.push(data.message);
        this.setState({messages:messages})
        console.log(e.data)
        
      }.bind(this)

    chatSocket.onclose = function(e) {
      console.error('Chat socket closed unexpectedly');
      let baseUrl = this.props.baseUrl;
      setTimeout(function() {
        let chatSocket = new WebSocket('ws://'+ baseUrl.replace("http://","")+ '/ws/chat/'+newRoom+'/'+"?token="+localStorage.getItem('token'));
      }, 1000);
    }.bind(this)

    chatSocket.onerror = function(err: any) {
      console.error('Socket encountered error: ', err.message, 'Closing socket');
      chatSocket.close();
    };

    document.querySelector("#submitButton").addEventListener("click", function() {
      let inputValue:string = (document.querySelector("#messageValue") as HTMLInputElement).value
      console.log(inputValue)
      if (inputValue != "") {
        chatSocket.send(JSON.stringify({'message': inputValue}));
      }
    }
    )
  }


    getFetch(endpoint:string, state: "messages" | "topics") {
      fetch(this.props.baseUrl + endpoint,  {
        headers: {Authorization: `JWT ${localStorage.getItem('token')}`}
      })
        .then(response => {
          if (response.status > 400) {
            return this.setState(() => {
              return { error: "Something went wrong!" };
            });
          }
          return response.json();
        })
        .then((data: string[]) => this.setState({...this.state, [state]: data})
        );
    }

    componentDidMount() {
      this.getFetch("/api/topics/", "topics")
    }

    render() {
      let messages = []
      this.state.messages  ? this.state.messages.forEach((item, index) =>
        messages.push(<Message text={item} user={true} key={index}/>)
      ) : null
      
      return (
        <div className="mx-auto shadow-lg rounded-lg mt-1 h-full">
            <div className="flex flex-row justify-between bg-white h-full">
            <div className="flex flex-col w-2/5 border-r-2 overflow-y-auto">
                <div className="border-b-2 py-4 px-2">
                <input value={this.state.roomName} onChange={(e) => {this.handleChange(e, "roomName")}} type="text" placeholder="search chatting" className="py-2 px-2 border-2 border-gray-200 rounded-2xl w-full"/>
                </div>
                {this.state.topics  ? this.state.topics.map(item =>
                  <Forum text={item.name} key={item.id} changeRoom={this.changeRoom}/>
                ) : null}
              
            </div>
            <div className="w-full px-5 flex flex-col justify-between">
                <div className="flex flex-col mt-5">
                    {messages}
                </div>
                <div className={"flex mb-12 " + (this.state.activeRoom ? "" : "hidden")}>
                  <input value={this.state.message} onChange={(e) => {this.handleChange(e, "message")}} className="w-full bg-gray-300 py-5 px-3 rounded-xl  flex-1" type="text" id="messageValue"/>
                  <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" id="submitButton">Submit</button>
                </div>
                </div>
            </div>
            </div>
  )
}
}

export default Chat;


//{this.state.messages ? this.state.messages.map((item, idx) => {
//  <Message text={item} user={true} key={idx}/>
//}):null}