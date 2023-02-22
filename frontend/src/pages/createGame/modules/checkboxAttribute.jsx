import React from "react"
import "./createGameStyles/checkboxAttribute.scss"

function CheckboxAttribute({ change, text, ...props }) {
	return (
		<div className="checkbox_attribute">
			<label className="custom-checkbox_attribute">
				<input
					className={"input_checkbox_attribute"}
					type="checkbox"
					onChange={(event) => {
						change(text, event.target.checked)
					}}
				/>
				<span className={"span_checkbox_attribute"}>{text}</span>
			</label>
		</div>
	)
}

export default CheckboxAttribute
