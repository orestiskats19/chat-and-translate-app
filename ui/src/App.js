import React, {useState, useEffect} from 'react';
import './App.css';
import Dropdown from "react-bootstrap/Dropdown";

import 'bootstrap/dist/css/bootstrap.min.css';
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Bubble from "./Bubble";

function App() {
    const [textValue, setTextValue] = useState("Please add your text here")
    const [language, setLanguage] = useState("english-input")
    const [messages, setMessages] = useState([
    ])

    useEffect(() => {

    }, []);

    const result = (option, question) => {
        fetch("/result", {
                method: "POST",
                cache: "no-cache",
                headers: {
                    "content_type": "application/json",
                },
                body: JSON.stringify({"option": option, "question": question})
            }
        ).then(response => {
            return response.text()
        }).then(json => setMessages([...messages, {
            "direction": ['left','right'][ Math.floor(Math.random()*2)],
            "text": textValue,
            "translation": json,
            "sequence": 1
        }]))
    }

    const handleChange = (event) => {
        setTextValue(event.target.value)
    }
    const languageTranslation = (lang) => {
        return {"english-input": "English to Spanish", "spanish-input": "Spanish to English"}[lang]
    }

    return (
        <div className="App">
            <div>Welcome to the Hugging Chat translator</div>
            <div className={"container"}>
                <Form className={"form"}>
                    <Form.Group controlId="exampleForm.ControlTextarea1">
                        <Form.Control className={"textarea"} as="textarea" onKeyPress={event => {
                            if (event.key === "Enter") {
                                handleChange.bind(this);
                                result(language, textValue)
                            }
                        } }  onChange={handleChange.bind(this)} rows="3"/>
                    </Form.Group>
                </Form>
                <div className={"button"}>
                    <Button variant="success" onClick={() => result(language, textValue)}>Send & translate</Button>
                </div>
                <div className={"dropdown"}>
                    <Dropdown className={"dropdown"}>
                        <Dropdown.Toggle variant="primary" id="dropdown-basic">
                            {languageTranslation(language)}
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item onClick={() => setLanguage("english-input")}>English to
                                Spanish</Dropdown.Item>
                            <Dropdown.Item onClick={() => setLanguage("spanish-input")}>Spanish to
                                English</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                </div>
            </div>
            <div>
            {messages.length > 0 ?
                messages.map(message => {
                    return <Bubble props={message}/>
                })
                : <></>}
            </div>
        </div>

    );
}

export default App;
