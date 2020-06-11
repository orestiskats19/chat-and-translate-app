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
    const [cookie, setCookie] = useState("")
    const [authorized, setAuthorized] = useState(false)

    useEffect(() => {
        checkLocalStorage()
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
        }, 5000);
        return () => clearInterval(interval);
    }, []);


    const storeUserInServer = () => {
        fetch("/postCookie", {
                method: "POST",
                cache: "no-cache",
                headers: {
                    "content_type": "application/json",
                }
            }
        ).then(r => {
            return r.json()
        }).then(res => {
            window.localStorage.setItem("hugging-translator-cookie", res["cookie"])
            setAuthorized(true)
        })

    }

    const checkLocalStorage = () => {
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
        }).then(r => {
            const cooks = r.substring(1, r.length - 1).replace(/ '/g, '').replace(/'/g, '').split(',')
            if (cooks.includes(window.localStorage.getItem("hugging-translator-cookie"))) {
                setAuthorized(true)
            } else {
                // if (cooks < 4) {
                storeUserInServer()
                // }
            }
        })

    }

    const scrollToBottom = async () => {
        const scrollingElement = (document.scrollingElement || document.body);
        scrollingElement.scrollTop = scrollingElement.scrollHeight;
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
                    "direction": window.localStorage.getItem("hugging-translator-cookie")
                })
            }
        ).then(response => {
            return response.text()
        }).then(json => setMessages([...messages, {
            "direction": window.localStorage.getItem("hugging-translator-cookie"),
            "text": textValue,
            "translation": json,
            "sequence": 1
        }]))
    }

    const handleChange = (event) => {
        setTextValue(event.target.value)
    }

    const languageTranslation = (lang) => {
        return supported_languages[lang]["name"]

    }
    const sendMessage = async () => {
        await result(language, textValue)
        await scrollToBottom()
        setTextValue("")
    }

    return (
        [authorized ?
            <div className="App">
                <div className={"container123"}>
                    <div className={"messages-container"}>
                        {messages.length > 0 ?
                            messages.map(message => {
                                return <Bubble props={message}/>
                            })
                            : <></>}
                    </div>

                    <div className={"text-area-container"}>
                        <Form className={"form"}>
                            <Form.Group controlId="exampleForm.ControlTextarea1">
                                <Form.Control value={textValue} className={"textarea"} as="textarea"
                                              onKeyPress={async event => {
                                                  if (event.key === "Enter") {
                                                      handleChange.bind(this);
                                                      await sendMessage()
                                                  }
                                              }} onChange={handleChange.bind(this)} rows="3"/>
                            </Form.Group>
                        </Form>
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
            : <> Sorry. You are not authorized to access this website at the moment </>]
    );
}

export default App;

//  "german-to-dutch": {
//    "model": "Helsinki-NLP/opus-mt-en-ROMANCE",
//    "target_language": "es",
//    "name": "English To Spanish"
//  },
//  "dutch-to-german": {
//    "model": "Helsinki-NLP/opus-mt-en-ROMANCE",
//    "target_language": "es",
//    "name": "English To Spanish"
//  },
//  "german-to-danish": {
//    "model": "Helsinki-NLP/opus-mt-en-ROMANCE",
//    "target_language": "es",
//    "name": "English To Spanish"
//  },
//  "danish-to-german": {
//    "model": "Helsinki-NLP/opus-mt-en-ROMANCE",
//    "target_language": "es",
//    "name": "English To Spanish"
//  },