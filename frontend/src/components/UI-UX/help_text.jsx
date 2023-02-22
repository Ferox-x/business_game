import React from "react"
import "./styles/help_text.css"
import { useNavigate } from "react-router-dom"

function HelpText({ text, link, ...props }) {
	const navigate = useNavigate()

	function redirectTo() {
		navigate(link)
	}

	return (
		<div
			className="help_text__container help_text__container_underline"
			{...props}
			onClick={() => {
				redirectTo()
			}}
		>
			{text}
		</div>
	)
}

export default HelpText
