import React from "react"
import "./styles/button.css"

function Button({ action, children, ...props }) {
	return (
		<div className="bs_button" onClick={action}>
			{children}
		</div>
	)
}

export default Button
