import React from "react"
import "./createGameStyles/checkboxAttribute.scss"

function CheckboxAttribute({
	initialState,
	value,
	change,
	text,
	attribute_id,
	...props
}) {
	if (value === undefined) {
		if (initialState === undefined) {
			value = false
		} else {
			value = initialState
		}
	}

	return (
		<div className="checkbox_attribute">
			<label className="custom-checkbox_attribute">
				<input
					className={"input_checkbox_attribute"}
					type="checkbox"
					checked={value}
					onChange={(event) => {
						change(attribute_id, event.target.checked)
					}}
				/>
				<span className={"span_checkbox_attribute"}>{text}</span>
			</label>
		</div>
	)
}

export default CheckboxAttribute
