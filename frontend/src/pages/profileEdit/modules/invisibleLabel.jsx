import React from "react"
import "../components/styles/formLabel.scss"

function InvisibleLabel(props) {
	return (
		<label className="form_label invisible" htmlFor="#">
			<input className="form_edit_input form_edit_input_attribute" type="#" id="#" />
		</label>
	)
}

export default InvisibleLabel
