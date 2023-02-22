import React from "react"
import "./genericEditStyles/formButton.scss"

function FormButton({ action, children, ...props }) {
	return (
		<div className={"btn_change_password_container form_label"}>
			<button
				className={"btn_reset btn_change_password"}
				onClick={(event) => {
					event.preventDefault()
					action()
				}}
			>
				{children}
			</button>
		</div>
	)
}

export default FormButton
