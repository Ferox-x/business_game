import React from "react"
import "./styles/formLabel.scss"

function FormLabelPassword({
	value,
	setValue,
	label,
	type,
	htmlFor,
	placeholder,
	...props
}) {
	return (
		<label className="form_label" htmlFor={htmlFor}>
			{label}
			<input
				className="form_edit_input"
				value={value}
				onChange={(event) => setValue(event.target.value)}
				type={type}
				id={htmlFor}
				placeholder={placeholder}
			/>
		</label>
	)
}

export default FormLabelPassword
