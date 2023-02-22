import React from "react"
import "./styles/formLabel.scss"

function FormLabel({
	variableName,
	setValue,
	value,
	label,
	type,
	placeholder,
	name,
	...props
}) {
	function changeFullName(event) {
		let newObjectFullName = { ...value }
		newObjectFullName[variableName] = event.target.value
		setValue(newObjectFullName)
	}

	return (
		<label className="form_label" htmlFor={variableName}>
			{label}
			<input
				className="form_edit_input"
				onChange={(event) => {
					changeFullName(event)
				}}
				value={value[variableName]}
				type={type}
				id={variableName}
				placeholder={placeholder}
			/>
		</label>
	)
}

export default FormLabel
