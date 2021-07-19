import React, { Component } from "react";

type formKeys = "roomName" | "message" | "search";

type topic = {
  id: number,
  name: string,
  created_at: Date,
}

type ForumProps = {
    item: topic,
    changeRoom: (item: topic) => void,
    getHighlighted: (text: string) => void,
  }

class Forum extends Component<ForumProps, {}> {

    render() {
      var text: any = this.props.getHighlighted(this.props.item.name)
      return (
        <div className="flex flex-row py-4 px-2 items-center border-b-2" onClick={() => this.props.changeRoom(this.props.item)}>
          <div className="w-full">
             {text}
          </div>
        </div>
  )
}
}

type MessageProps = {
    text: string,
    same: boolean,
  }

class Message extends Component<MessageProps, {}> {

    render() {
        let firstDiv = this.props.same ? "justify-end" : "justify-start"
        let secondDiv = this.props.same ? "mr-2  bg-blue-400 rounded-bl-3xl rounded-tl-3xl rounded-tr-xl" 
        : "ml-2 bg-gray-400 rounded-br-3xl rounded-tr-3xl rounded-tl-xl"
      return (
        <div className={"flex mb-4 " + firstDiv}>
            <div className={"text-white py-3 px-4 " + secondDiv}>
            {this.props.text}
            </div>
        </div>
  )
  }
}

type message = {
  text: string,
  same: boolean,
  topic: topic,
  user: number,
}

type messageResponse = {
  count: number,
  next: string,
  previous: string,
  results: message[],
}

type ChatState = {
    roomName: string,
    activeRoom: string,
    messageResponse: messageResponse,
    topics: topic[],
    message: string,
    error: string,
    search: string
}

type ChatProps = {
  baseUrl: string,
  userId: number
}


class Chat extends Component<ChatProps, ChatState> {
    constructor(props: any) {
        super(props);
        this.state = {
            roomName: '',
            activeRoom: '',
            messageResponse: null,
            topics: [],
            message: '',
            error: '',
            search: ''
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleLoad = this.handleLoad.bind(this);
        this.changeRoom = this.changeRoom.bind(this);
        this.getHighlighted = this.getHighlighted.bind(this);
      }

    handleChange(e: any, formKey: formKeys) {this.setState({...this.state, [formKey]: e.target.value})};

    dynamicSearch() {
      return this.state.topics.filter((item: topic) => item.name.toLowerCase().includes(this.state.search.toLowerCase()));
    }

  handleLoad() {

    if (this.state.messageResponse.previous) {
      var arrURL: string[] = this.state.messageResponse.previous.split("/backend");
      var URL: string = arrURL[0]+":1337/backend"+arrURL[1];
      fetch(URL,  {
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
      .then((data:messageResponse) => {
        var currentMess: messageResponse = this.state.messageResponse;
        var newMess: messageResponse = {count: null, next: null, previous: null, results: []};
        newMess.count = data.count;
        newMess.next = data.next;
        newMess.previous = data.previous;
        newMess.results = data.results.concat(currentMess.results);
        this.setState({messageResponse: newMess});
      });
    } else {
      console.log("No more messages to load")
      }
    }
  

    getHighlighted(text: string) {
      var no_match: string = "text-lg font-semibold"
      var match: string = "text-lg font-semibold bg-yellow-400"
      if (this.state.search) {
        const parts = text.split(new RegExp(`(${this.state.search})`, 'gi'));
        return <span> { parts.map((part, i) => 
            <span key={i} className={part.toLowerCase() === this.state.search.toLowerCase() ? match : no_match }>
                { part }
            </span>)
        } </span>;
      } else {
        return  <span className={no_match}>{text}</span>
      }
  }

    chatSocket: any = ""

    changeRoom(item:topic) {
      if (item.name != this.state.activeRoom) {
        this.setState({activeRoom: item.name})
        this.getFetch("/api/messages?topic="+item.id+"&page=last", "messageResponse")
        if (this.chatSocket != "") {
          this.chatSocket.close()
        }
        this.chatSocket = new WebSocket('ws://'+ this.props.baseUrl.replace("http://","").replace("/backend","") + 
        '/ws/chat/'+item.name+'/'+"?token="+localStorage.getItem('token'));
        this.chatSocket.onmessage = function(e) {
          
          const data = JSON.parse(e.data);
          const messages = this.state.messageResponse;
          messages.results.push({text:data.message,user:data.user_id,topic:data.topic});
          this.setState({messageResponse:messages})
          console.log(e.data)
          
        }.bind(this)

      this.chatSocket.onclose = function(e) {
        let baseUrl = this.props.baseUrl;
        setTimeout(function() {
          let chatSocket = new WebSocket('ws://'+ baseUrl.replace("http://","").replace("/backend","") + 
          '/ws/chat/'+item.name+'/'+"?token="+localStorage.getItem('token'));
        }, 1000);
      }.bind(this)

      this.chatSocket.onerror = function(err: any) {
        this.chatSocket.close();
      }.bind(this);
    }
  }

  gotoBottom(selector:string){
    let item = document.querySelector(selector)
    if (item) {
      item.scrollIntoView ({ behavior: "smooth" });
    }
 }

  handleSubmit() {
    if (this.state.message) {
      let message = this.state.message
      this.setState({message:""}, function() {
        this.chatSocket.send(JSON.stringify({'message': message}));
      })
    }
  }

  getFetch(endpoint:string, state: "messageResponse" | "topics") {
      fetch(this.props.baseUrl + endpoint,  {
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
      .then((data: string[]) => this.setState({...this.state, [state]: data})
      );
  }

    componentDidMount() {
      this.getFetch("/api/topics/", "topics")
    }

    componentDidUpdate() {
      this.gotoBottom(".messageContainer")
    }

    render() {
      let messages = []
      this.state.messageResponse  ? this.state.messageResponse.results.forEach((item, index) =>
        messages.push(<Message text={item.text} same={item.user==this.props.userId} key={index}/>)
      ) : null
      var searchReturn = this.state.topics ? this.dynamicSearch() : null
      
      return (
        <div className="mx-auto shadow-lg rounded-lg mt-1 h-full">
            <div className="flex flex-row justify-between bg-white h-full">
            <div className="flex flex-col w-2/5 border-r-2 overflow-y-auto">
                <div className="border-b-2 py-4 px-2">
                <input value={this.state.search} onChange={(e) => {this.handleChange(e, "search")}} type="text" placeholder="Search topics" 
                className="py-2 px-2 border-2 border-gray-200 rounded-2xl w-full"/>
                </div>
                {searchReturn ? searchReturn.map(item =>
                  <Forum item={item} key={item.id} changeRoom={this.changeRoom} getHighlighted={this.getHighlighted}/>
                ) : null}
              
            </div>
            <div className="w-full px-5 flex flex-col justify-between">
                <div className="flex flex-col mt-5 overflow-scroll ">
                  {this.state.activeRoom ? <p onClick={this.handleLoad} className="text-blue-500 underline text-center cursor-pointer">Load More Messages</p> : null}
                    {messages}
                    <div className="messageContainer"></div>
                </div>
                <div className={"flex mb-4 " + (this.state.activeRoom ? "" : "hidden")}>
                  <input value={this.state.message} onChange={(e) => {this.handleChange(e, "message")}} 
                  className="w-full bg-gray-300 py-5 px-3 rounded-xl  flex-1" type="text" id="messageValue"/>
                  <button onClick={this.handleSubmit} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Submit</button>
                </div>
                </div>
            </div>
          </div>
    )
  }
}

export default Chat;