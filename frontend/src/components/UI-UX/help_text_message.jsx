import React from "react"
import HelpText from "./help_text"
import "./styles/help_text.css"

function HelpTextMessage({ message, text, link, ...props }) {
	return (
		<div className="help_text_container">
			<div className="help_text_container_message login_page__forgot_password-space">
				{message}
			</div>
			<HelpText link={link} text={text} />
		</div>
	)
}

export default HelpTextMessage
