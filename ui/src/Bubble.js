import React, {useState, useEffect} from 'react';
import './Bubble.css';
import Flag from 'react-world-flags'

function Bubble(message) {

    return <>
        <div className={"http://localhost:3000/"}>
            <li className={message.props.direction === "master" ? "me" : "him"}>
                <div className={"test"}>
                    <div className={"line"}>{message.props.text}</div>
                    <div className={"translation"}>
                        {message.props.translation}
                        <Flag code="por" height="16"/>
                    </div>
                </div>
            </li>
        </div>
    </>
}

export default Bubble;
