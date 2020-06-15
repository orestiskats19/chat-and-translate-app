import React, {useState, useEffect} from 'react';
import './App.css';
import Dropdown from "react-bootstrap/Dropdown";
import 'bootstrap/dist/css/bootstrap.min.css';
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Bubble from "./Bubble";
import supported_languages from './recourses/supported_languages.json'


function App() {
    const [textValue, setTextValue] = useState("")
    const [language, setLanguage] = useState("english-to-spanish")
    const [messages, setMessages] = useState([])
    const [authorized, setAuthorized] = useState(false)
    const [role, setRole] = useState("")
    const [predictedTokens, setPredictedTokens] = useState([])

    useEffect(() => {
        getUserRole()
        const interval = setInterval(() => {
            fetch("/getMessages", {
                    method: "GET",
                    headers: {
                        "content_type": "application/json",
                        'Accept': 'application/json'
                    }
                }
            ).then(response => {
                return response.json()
            }).then(res => {
                setMessages(res["messages"])
                scrollToBottom()
            })
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    const getUserRole = () => {
        fetch("/postCookies", {
                method: "POST",
                headers: {
                    "content_type": "application/json",
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                "cookie": window.localStorage.getItem('hugging-chat-translator')
            })
            }
        ).then(response => {
            return response.json()
        }).then(res => {
            return res["cookies"]
        }).then(res => {
            if (res['role'] !== "") {
                setRole(res["role"])
                window.localStorage.setItem('hugging-chat-translator', res["cookie"])
                setAuthorized(true)
            } else {
                setAuthorized(false)
            }
        })
    }

    const postCookie = () => {
        fetch("/getCookies", {
                method: "GET",
                headers: {
                    "content_type": "application/json"
                }
            }
        ).then(response => {
            return response.json()
        }).then(res => {
            return res["cookies"]
        }).then(res => {
            if (res !== "") {
                setRole(res)
                setAuthorized(true)
            } else {
                setAuthorized(true)
            }
        })
    }

    const scrollToBottom = async () => {
        const scrollingElement = (document.scrollingElement || document.body);
        scrollingElement.scrollTop = scrollingElement.scrollHeight;
    }

    const nextWordPredictor = (text) => {
        fetch("/next_word_predictor", {
                method: "POST",
                cache: "no-cache",
                headers: {
                    "content_type": "application/json",
                },
                body: JSON.stringify({
                    "text": text,
                })
            }
        ).then(response => {
            return response.json()
        }).then(res => {
            return res["tokens"]
        }).then(res => setPredictedTokens([res]))
    }

    const result = (option, text) => {
        fetch("/result", {
                method: "POST",
                cache: "no-cache",
                headers: {
                    "content_type": "application/json",
                },
                body: JSON.stringify({
                    "option": option,
                    "text": text,
                    "direction": role
                })
            }
        ).then(response => {
            return response["translation"]
        }).then(json => setMessages([...messages, {
            "direction": role,
            "text": textValue,
            "translation": json,
        }]))
    }

    const handleChange = (event) => {
        setTextValue(event.target.value)
        nextWordPredictor(textValue)
    }

    const languageTranslation = (lang) => {
        return supported_languages[lang]["name"]
    }

    const sendMessage = async () => {
        if (textValue !== "") {
            await result(language, textValue)
            await scrollToBottom()
            setTextValue("")
        }
    }

    return (
        [authorized ?
            <div className="App">
                <div className={"app-container"}>
                    <div className={"messages-container"}>
                        {messages.length > 0 ?
                            messages.map(message => {
                                return <Bubble props={message}/>
                            })
                            : <></>}
                    </div>
                    <div className={"text-area-container"}>
                        <div className={"input-and-next-tokens"}>
                            <div className={"token-container"}>{predictedTokens.map(tokens => {
                                return tokens.map(token => {
                                    return <div className={"predicted-tokens"}>
                                        <Button variant={"secondary"} size="sm" onClick={()=>{
                                            setTextValue(textValue + token)
                                            nextWordPredictor(textValue)
                                        }}>{token}</Button></div>
                                })
                            })}</div>
                            <Form className={"form"}>
                                <Form.Group controlId="exampleForm.ControlTextarea1">
                                    <Form.Control value={textValue} className={"textarea"} as="textarea"
                                                  onKeyPress={async event => {
                                                      if (event.key === "Enter") {
                                                          event.preventDefault();
                                                          await sendMessage()
                                                      }
                                                  }} onChange={handleChange.bind(this)} rows="3"/>
                                </Form.Group>
                            </Form>
                        </div>
                        <div className={"buttons"}>
                            <div className={"button"}>
                                <Button variant="success" onClick={async () => {
                                    await sendMessage()
                                }}>Send &
                                    translate</Button>
                            </div>
                            <div className={"dropdown"}>
                                <Dropdown className={"dropdown"}>
                                    <Dropdown.Toggle variant="primary" id="dropdown-basic">
                                        {languageTranslation(language)}
                                    </Dropdown.Toggle>
                                    <Dropdown.Menu>
                                        {Object.keys(supported_languages).map((supported_language) => {
                                            return <Dropdown.Item onClick={() => setLanguage(supported_language)}>
                                                {supported_languages[supported_language]["name"]}
                                            </Dropdown.Item>
                                        })}
                                    </Dropdown.Menu>
                                </Dropdown>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            : <> Sorry, you are not authorized to access this website at the moment. </>]
    );
}

export default App;
