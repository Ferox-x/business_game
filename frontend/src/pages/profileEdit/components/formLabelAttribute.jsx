import React from "react"
import "./styles/formLabel.scss"

function FormLabelAttribute({
	htmlFor,
	attributesAndValue,
	setAttributesAndValue,
	label,
	type,
	placeholder,
	name,
	...props
}) {
	function changeValueAttribute(event) {
		let newObjectAttributesAndValue = { ...attributesAndValue }
		newObjectAttributesAndValue[htmlFor] = event.target.value
		setAttributesAndValue(newObjectAttributesAndValue)
		console.log(attributesAndValue)
	}

	return (
		<label className="form_label form_label_attribute" htmlFor={htmlFor}>
			{label}
			<input
				className="form_edit_input form_edit_input_attribute"
				onChange={(event) => {
					changeValueAttribute(event)
				}}
				type={type}
				id={htmlFor}
				placeholder={placeholder}
			/>
		</label>
	)
}

export default FormLabelAttribute
